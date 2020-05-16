from PyQt5.QtGui import QPixmap,QPainter,QFont,QCursor,QMovie,QTextCursor,QColor,QPen
from PyQt5.QtCore import QThread,QDir, pyqtSignal,QTimer,QTime,Qt,QRect
from PyQt5.QtWidgets import (QPlainTextEdit,QHeaderView,QScroller,QAbstractItemView,QComboBox,QGraphicsDropShadowEffect,QWidget,QMainWindow,QFrame,
  QApplication, QDialog,QProgressBar, QPushButton,QMdiSubWindow,
  QTreeWidget,QLabel,QLineEdit,QTreeWidgetItem,
  QMdiArea,QGraphicsView,QInputDialog, QLineEdit, QFileDialog,QSizePolicy,QHBoxLayout,QScrollArea,QVBoxLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic
import sys
import os
from argparse import Namespace
import argparse
import youtube_dl
import cv2
import time
import tqdm
import numpy
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.video.fx.all import crop
from moviepy.editor import AudioFileClip, clips_array, TextClip, CompositeVideoClip
import shutil
from pathlib import Path
import sys
sys.path.append('faceswap')

from lib.utils import FullHelpArgumentParser
from scripts.extract import ExtractTrainingData
from scripts.train import TrainingProcessor
from scripts.convert import ConvertImage
from lib.faces_detect import detect_faces
from plugins.PluginLoader import PluginLoader
from lib.FaceFilter import FaceFilter

class FaceIt:
    VIDEO_PATH = 'data/videos'
    PERSON_PATH = 'data/persons'
    PROCESSED_PATH = 'data/processed'
    OUTPUT_PATH = 'data/output'
    MODEL_PATH = 'models'
    MODELS = {}

    @classmethod
    def add_model(cls, model):
        FaceIt.MODELS[model._name] = model
    
    def __init__(self, name, person_a, person_b):
        def _create_person_data(person):
            return {
                'name' : person,
                'videos' : [],
                'faces' : os.path.join(FaceIt.PERSON_PATH, person + '.jpg'),
                'photos' : []
            }
        
        self._name = name

        self._people = {
            person_a : _create_person_data(person_a),
            person_b : _create_person_data(person_b),
        }
        self._person_a = person_a
        self._person_b = person_b
        
        self._faceswap = FaceSwapInterface()

        if not os.path.exists(os.path.join(FaceIt.VIDEO_PATH)):
            os.makedirs(FaceIt.VIDEO_PATH)            

    def add_photos(self, person, photo_dir):
        self._people[person]['photos'].append(photo_dir)
            
    def add_video(self, person, name, url=None, fps=20):
        self._people[person]['videos'].append({
            'name' : name,
            'url' : url,
            'fps' : fps
        })

    def fetch(self):
        self._process_media(self._fetch_video)

    def extract_frames(self):
        self._process_media(self._extract_frames)

    def extract_faces(self):        
        self._process_media(self._extract_faces)
        self._process_media(self._extract_faces_from_photos, 'photos')        

    def all_videos(self):
        return self._people[self._person_a]['videos'] + self._people[self._person_b]['videos']

    def _process_media(self, func, media_type = 'videos'):
        for person in self._people:
            for video in self._people[person][media_type]:
                func(person, video)

    def _video_path(self, video):
        return os.path.join(FaceIt.VIDEO_PATH, video['name'])        

    def _video_frames_path(self, video):
        return os.path.join(FaceIt.PROCESSED_PATH, video['name'] + '_frames')        

    def _video_faces_path(self, video):
        return os.path.join(FaceIt.PROCESSED_PATH, video['name'] + '_faces')

    def _model_path(self, use_gan = False):
        path = FaceIt.MODEL_PATH
        if use_gan:
            path += "_gan"
        return os.path.join(path, self._name)

    def _model_data_path(self):
        return os.path.join(FaceIt.PROCESSED_PATH, "model_data_" + self._name)
    
    def _model_person_data_path(self, person):
        return os.path.join(self._model_data_path(), person)

    def _fetch_video(self, person, video):
        options = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
            'outtmpl': os.path.join(FaceIt.VIDEO_PATH, video['name']),
            'merge_output_format' : 'mp4'
        }
        #with youtube_dl.YoutubeDL(options) as ydl:
            #x = ydl.download([video['url']])

    def _extract_frames(self, person, video):
        video_frames_dir = self._video_frames_path(video)
        video_clip = VideoFileClip(self._video_path(video))
        
        start_time = time.time()
        print('[extract-frames] about to extract_frames for {}, fps {}, length {}s'.format(video_frames_dir, video_clip.fps, video_clip.duration))
        
        if os.path.exists(video_frames_dir):
            print('[extract-frames] frames already exist, skipping extraction: {}'.format(video_frames_dir))
            return
        
        os.makedirs(video_frames_dir)
        frame_num = 0
        for frame in tqdm.tqdm(video_clip.iter_frames(fps=video['fps']), total = video_clip.fps * video_clip.duration):
            video_frame_file = os.path.join(video_frames_dir, 'frame_{:03d}.jpg'.format(frame_num))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Swap RGB to BGR to work with OpenCV
            cv2.imwrite(video_frame_file, frame)
            frame_num += 1

        print('[extract] finished extract_frames for {}, total frames {}, time taken {:.0f}s'.format(
            video_frames_dir, frame_num-1, time.time() - start_time))            

    def _extract_faces(self, person, video):
        video_faces_dir = self._video_faces_path(video)

        start_time = time.time()
        print('[extract-faces] about to extract faces for {}'.format(video_faces_dir))
        
        if os.path.exists(video_faces_dir):
            print('[extract-faces] faces already exist, skipping face extraction: {}'.format(video_faces_dir))
            return
        
        os.makedirs(video_faces_dir)
        self._faceswap.extract(self._video_frames_path(video), video_faces_dir, self._people[person]['faces'])

    def _extract_faces_from_photos(self, person, photo_dir):
        photo_faces_dir = self._video_faces_path({ 'name' : photo_dir })

        start_time = time.time()
        print('[extract-faces] about to extract faces for {}'.format(photo_faces_dir))
        
        if os.path.exists(photo_faces_dir):
            print('[extract-faces] faces already exist, skipping face extraction: {}'.format(photo_faces_dir))
            return
        
        os.makedirs(photo_faces_dir)
        self._faceswap.extract(self._video_path({ 'name' : photo_dir }), photo_faces_dir, self._people[person]['faces'])


    def preprocess(self):
        self.fetch()
        self.extract_frames()
        self.extract_faces()
    
    def _symlink_faces_for_model(self, person, video):
        if isinstance(video, str):
            video = { 'name' : video }
        for face_file in os.listdir(self._video_faces_path(video)):
            target_file = os.path.join(self._model_person_data_path(person), video['name'] + "_" + face_file)
            face_file_path = os.path.join(os.getcwd(), self._video_faces_path(video), face_file)
            os.symlink(face_file_path, target_file)

    def train(self, use_gan = False):
        # Setup directory structure for model, and create one director for person_a faces, and
        # another for person_b faces containing symlinks to all faces.
        if not os.path.exists(self._model_path(use_gan)):
            os.makedirs(self._model_path(use_gan))

        if os.path.exists(self._model_data_path()):
            shutil.rmtree(self._model_data_path())

        for person in self._people:
            os.makedirs(self._model_person_data_path(person))
        self._process_media(self._symlink_faces_for_model)

        self._faceswap.train(self._model_person_data_path(self._person_a), self._model_person_data_path(self._person_b), self._model_path(use_gan), use_gan)

    def convert(self, video_file, swap_model = False, duration = None, start_time = None, use_gan = False, face_filter = False, photos = True, crop_x = None, width = None, side_by_side = False):
        # Magic incantation to not have tensorflow blow up with an out of memory error.
        import tensorflow as tf
        import keras.backend.tensorflow_backend as K
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        config.gpu_options.visible_device_list="0"
        K.set_session(tf.Session(config=config))

        # Load model
        model_name = "Original"
        converter_name = "Masked"
        if use_gan:
            model_name = "GAN"
            converter_name = "GAN"
        model = PluginLoader.get_model(model_name)(Path(self._model_path(use_gan)))
        if not model.load(swap_model):
            print('model Not Found! A valid model must be provided to continue!')
            exit(1)

        # Load converter
        converter = PluginLoader.get_converter(converter_name)
        converter = converter(model.converter(False),
                              blur_size=8,
                              seamless_clone=True,
                              mask_type="facehullandrect",
                              erosion_kernel_size=None,
                              smooth_mask=True,
                              avg_color_adjust=True)

        # Load face filter
        filter_person = self._person_a
        if swap_model:
            filter_person = self._person_b
        filter = FaceFilter(self._people[filter_person]['faces'])

        # Define conversion method per frame
        def _convert_frame(frame, convert_colors = True):
            if convert_colors:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Swap RGB to BGR to work with OpenCV
            for face in detect_faces(frame, "cnn"):
                if (not face_filter) or (face_filter and filter.check(face)):
                    frame = converter.patch_image(frame, face)
                    frame = frame.astype(numpy.float32)
            if convert_colors:                    
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Swap RGB to BGR to work with OpenCV
            return frame
        def _convert_helper(get_frame, t):
            return _convert_frame(get_frame(t))

        media_path = self._video_path({ 'name' : video_file })
        if not photos:
            # Process video; start loading the video clip
            video = VideoFileClip(media_path)

            # If a duration is set, trim clip
            if duration:
                video = video.subclip(start_time, start_time + duration)
            
            # Resize clip before processing
            if width:
                video = video.resize(width = width)

            # Crop clip if desired
            if crop_x:
                video = video.fx(crop, x2 = video.w / 2)

            # Kick off convert frames for each frame
            new_video = video.fl(_convert_helper)

            # Stack clips side by side
            if side_by_side:
                def add_caption(caption, clip):
                    text = (TextClip(caption, font='Amiri-regular', color='white', fontsize=80).
                            margin(40).
                            set_duration(clip.duration).
                            on_color(color=(0,0,0), col_opacity=0.6))
                    return CompositeVideoClip([clip, text])
                video = add_caption("Original", video)
                new_video = add_caption("Swapped", new_video)                
                final_video = clips_array([[video], [new_video]])
            else:
                final_video = new_video

            # Resize clip after processing
            #final_video = final_video.resize(width = (480 * 2))

            # Write video
            output_path = os.path.join(self.OUTPUT_PATH, video_file)
            final_video.write_videofile(output_path, rewrite_audio = True)
            
            # Clean up
            del video
            del new_video
            del final_video
        else:
            # Process a directory of photos
            for face_file in os.listdir(media_path):
                face_path = os.path.join(media_path, face_file)
                image = cv2.imread(face_path)
                image = _convert_frame(image, convert_colors = False)
                cv2.imwrite(os.path.join(self.OUTPUT_PATH, face_file), image)

class FaceSwapInterface:
    def __init__(self):
        self._parser = FullHelpArgumentParser()
        self._subparser = self._parser.add_subparsers()

    def extract(self, input_dir, output_dir, filter_path):
        extract = ExtractTrainingData(
            self._subparser, "extract", "Extract the faces from a pictures.")
        args_str = "extract --input-dir {} --output-dir {} --processes 1 --detector cnn --filter {}"
        args_str = args_str.format(input_dir, output_dir, filter_path)
        self._run_script(args_str)

    def train(self, input_a_dir, input_b_dir, model_dir, gan = False):
        model_type = "Original"
        if gan:
            model_type = "GAN"
        train = TrainingProcessor(
            self._subparser, "train", "This command trains the model for the two faces A and B.")
        args_str = "train --input-A {} --input-B {} --model-dir {} --trainer {} --batch-size {} --write-image"
        args_str = args_str.format(input_a_dir, input_b_dir, model_dir, model_type, 16)
        self._run_script(args_str)

    def _run_script(self, args_str):
        args = self._parser.parse_args(args_str.split(' '))
        args.func(args)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.i=0
        self.i1=0
        self.initUI()


    def initUI(self):

        self.scroll = QScrollArea(self)             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget1 = QWidget(self)
        self.widget1.setStyleSheet('background-color:#FAF6F5;')
        self.widget1.resize(1024,1800)
        # self.widget2=QWidget(self)
        # self.widget2.setStyleSheet('background-color:black;')
        # self.widget2.resize(1024,800)
        # self.widget2.move(0,500) 
        self.setGeometry(100,100,1024,768)
        #self.vbox = QVBoxLayout()
        #self.widget1.setLayout(self.vbox)                # Widget that contains the collection of Vertical Box
        self.epf = QLabel("",self.widget1)
        effect = QGraphicsDropShadowEffect(self.epf)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        self.epf.setGraphicsEffect(effect)
        self.epf.setStyleSheet(("QLabel{background-color:white; color: white;padding-left:8px;border-style: ridge;border-width:0px;border-radius: 10px;border-color: #008CBA;}"))
        #self.epf.setStyleSheet('background-color:#4299ff;padding-left:10px;')
        self.epf.setGeometry(4, 3,1000,60)

        self.epf1 = QLabel("",self.widget1)
        #self.epf.setFont(QFont('Arial', 18))
        effect = QGraphicsDropShadowEffect(self.epf1)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        self.epf1.setGraphicsEffect(effect)
        self.epf1.setStyleSheet(("QLabel{background-color:#FCFCFE; color: white;padding-left:8px;border-style: ridge;border-width:0px;border-radius: 10px;border-color: #008CBA;}"))
        #self.epf.setStyleSheet('background-color:#4299ff;padding-left:10px;')
        self.epf1.setGeometry(20, 93,970,1680)
        source_label=QLabel("Face Swap Using Hard Drive Videos",self.widget1)
        source_label.setStyleSheet('background-color:#FCFCFE;')
        source_label.setFont(QFont('Arial', 22))
        source_label.setGeometry(250,113,600,35)

        qq=u'\u2190'
        bb = QPushButton(qq+' Back', self.widget1)
        bb.setGeometry(20,3,85,58)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (18)
        bb.setFont(font)
        bb.setStyleSheet(("QPushButton{background-color:white; color: black;border-style: ridge;border-width:0px;border-radius: 0px;border-color: white;}"))
        #bb.clicked.connect(self.bb_onClick)
        self.epf = QLabel("",self.widget1)
        #self.epf.setFont(QFont('Arial', 18))
        effect = QGraphicsDropShadowEffect(self.epf)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        self.epf.setGraphicsEffect(effect)
        self.epf.setStyleSheet(("QLabel{background-color:white; color: white;padding-left:8px;border-style: ridge;border-width:0px;border-radius: 10px;border-color: #008CBA;}"))
        #self.epf.setStyleSheet('background-color:#4299ff;padding-left:10px;')
        self.epf.setGeometry(50, 163,900,420)
        source_label=QLabel("Add Source Videos",self.widget1)
        source_label.setStyleSheet('background-color:white;')
        source_label.setFont(QFont('Arial', 21))
        source_label.setGeometry(100,175,600,30)
        self.add_svideo = QPushButton('+', self.widget1)
        self.add_svideo.setGeometry(850,213,40,40)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (18)
        self.add_svideo.setFont(font)
        self.add_svideo.setStyleSheet(("QPushButton{background-color:red; color: black;border-style: ridge;border-width:0px;border-radius: 20px;border-color: white;}"))
        self.add_svideo.clicked.connect(self.add_svideo_onClick)

        self.del_svideo = QPushButton('-', self.widget1)
        self.del_svideo.setGeometry(800,213,40,40)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (28)
        self.del_svideo.setFont(font)
        self.del_svideo.setStyleSheet(("QPushButton{background-color:blue; color: black;border-style: ridge;border-width:0px;border-radius: 20px;border-color: white;}"))
        self.del_svideo.clicked.connect(self.del_svideo_onClick)
        

        self.dataView = QTreeWidget(self.widget1)
        self.dataView.setRootIsDecorated(False)
        self.dataView.setHeaderLabels(['Ref No','Source Videos'])
        self.dataView.header().setStyleSheet('padding-top:-2px;background-color:white;font-size:21pt; font-family: Arial;border-width:1px;border-style:outset;border-color:black; ')
        self.dataView.setColumnCount(2)
        self.dataView.setColumnWidth(0,100)
        self.dataView.setColumnWidth(1,100)

        self.dataView.setStyleSheet('background-color:white;color: black;')
        self.dataView.setFont(QFont('Times New Roman', 22))

        self.dataView.setGeometry(100,260,800,265)
        #self.dataView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        QScroller.grabGesture(self.dataView.viewport(), QScroller.TouchGesture)
        #self.dataView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        #self.dataView.itemClicked.connect(self.onItemClicked)



        self.epf = QLabel("",self.widget1)
        #self.epf.setFont(QFont('Arial', 18))
        effect = QGraphicsDropShadowEffect(self.epf)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        self.epf.setGraphicsEffect(effect)
        self.epf.setStyleSheet(("QLabel{background-color:white; color: white;padding-left:8px;border-style: ridge;border-width:0px;border-radius: 10px;border-color: #008CBA;}"))
        #self.epf.setStyleSheet('background-color:#4299ff;padding-left:10px;')
        self.epf.setGeometry(50, 603,900,420)
        source_label=QLabel("Add Destination Videos",self.widget1)
        source_label.setStyleSheet('background-color:white;')
        source_label.setFont(QFont('Arial', 22))
        source_label.setGeometry(100,613,600,30)
        self.add_dvideo = QPushButton('+', self.widget1)
        self.add_dvideo.setGeometry(850,653,40,40)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (18)
        self.add_dvideo.setFont(font)
        self.add_dvideo.setStyleSheet(("QPushButton{background-color:red; color: black;border-style: ridge;border-width:0px;border-radius: 20px;border-color: white;}"))
        self.add_dvideo.clicked.connect(self.add_dvideo_onClick)

        self.del_dvideo = QPushButton('-', self.widget1)
        self.del_dvideo.setGeometry(800,653,40,40)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (28)
        self.del_dvideo.setFont(font)
        self.del_dvideo.setStyleSheet(("QPushButton{background-color:blue; color: black;border-style: ridge;border-width:0px;border-radius: 20px;border-color: white;}"))
        self.del_dvideo.clicked.connect(self.del_dvideo_onClick)
        

        self.dataView1 = QTreeWidget(self.widget1)
        self.dataView1.setRootIsDecorated(False)
        self.dataView1.setHeaderLabels(['Ref No','Destination Videos'])
        self.dataView1.header().setStyleSheet('padding-top:-2px;background-color:white;font-size:21pt; font-family: Arial;border-width:1px;border-style:outset;border-color:black; ')
        self.dataView1.setColumnCount(2)
        self.dataView1.setColumnWidth(0,100)
        self.dataView1.setColumnWidth(1,100)

        self.dataView1.setStyleSheet('background-color:white;color: black;')
        self.dataView1.setFont(QFont('Times New Roman', 22))

        self.dataView1.setGeometry(100,700,800,265)
        
        source_label=QLabel("Picture of Person In Source Video",self.widget1)
        source_label.setFont(QFont('Arial', 22))
        source_label.setStyleSheet('background-color:#FCFCFE;')
        source_label.setGeometry(100,1113,600,30)
        self.lineEdit3 = QLineEdit(self.widget1)
        self.lineEdit3.setEnabled(False)
        self.lineEdit3.setFont(QFont('Arial', 11))
        self.lineEdit3.setGeometry(100, 1160, 650, 40)
        self.lineEdit3.setStyleSheet("background-color:white;color:black;")
        self.lineEdit3.setObjectName("lineEdit3")

        self.srcvideo_b = QPushButton('Select File', self.widget1)
        self.srcvideo_b.setGeometry(790,1155,120,50)
        effect = QGraphicsDropShadowEffect(self.srcvideo_b)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        self.srcvideo_b.setGraphicsEffect(effect)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (13)
        self.srcvideo_b.setFont(font)
        self.srcvideo_b.setStyleSheet(("QPushButton{background-color:#333335; color: white;border-style: ridge;border-width:0px;border-radius: 3px;border-color: #008CBA;}"))
        self.srcvideo_b.clicked.connect(self.srcvideo_b_onClick)

        source_label=QLabel("Picture of Person In Destination Video",self.widget1)
        source_label.setFont(QFont('Arial', 22))
        source_label.setStyleSheet('background-color:#FCFCFE;')
        source_label.setGeometry(100,1213,600,30)
        self.lineEdit4 = QLineEdit(self.widget1)
        self.lineEdit4.setEnabled(False)
        self.lineEdit4.setFont(QFont('Arial', 11))
        self.lineEdit4.setGeometry(100, 1260, 650, 40)
        self.lineEdit4.setStyleSheet("background-color:white;color:black;")
        self.lineEdit4.setObjectName("lineEdit4")

        self.dstvideo_b = QPushButton('Select File', self.widget1)
        self.dstvideo_b.setGeometry(790,1255,120,50)
        effect = QGraphicsDropShadowEffect(self.dstvideo_b)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        self.dstvideo_b.setGraphicsEffect(effect)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (13)
        self.dstvideo_b.setFont(font)
        self.dstvideo_b.setStyleSheet(("QPushButton{background-color:#333335; color: white;border-style: ridge;border-width:0px;border-radius: 3px;border-color: #008CBA;}"))
        self.dstvideo_b.clicked.connect(self.dstvideo_b_onClick)

        source_label=QLabel("Output Video in which face is to be replaced",self.widget1)
        source_label.setStyleSheet('background-color:#FCFCFE;')
        source_label.setFont(QFont('Arial', 22))
        source_label.setGeometry(100,1313,600,30)
        self.lineEdit5 = QLineEdit(self.widget1)
        self.lineEdit5.setEnabled(False)
        self.lineEdit5.setFont(QFont('Arial', 11))
        self.lineEdit5.setGeometry(100, 1360, 650, 40)
        self.lineEdit5.setStyleSheet("background-color:white;color:black;")
        self.lineEdit5.setObjectName("lineEdit5")

        self.output_v = QPushButton('Select File', self.widget1)
        self.output_v.setGeometry(790,1355,120,50)
        effect = QGraphicsDropShadowEffect(self.output_v)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        self.output_v.setGraphicsEffect(effect)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (13)
        self.output_v.setFont(font)
        self.output_v.setStyleSheet(("QPushButton{background-color:#333335; color: white;border-style: ridge;border-width:0px;border-radius: 3px;border-color: #008CBA;}"))
        self.output_v.clicked.connect(self.output_v_onClick)

        source_label=QLabel("Output Directory",self.widget1)
        source_label.setStyleSheet('background-color:#FCFCFE;')
        source_label.setFont(QFont('Arial', 22))
        source_label.setGeometry(100,1413,600,30)
        self.lineEdit6 = QLineEdit(self.widget1)
        self.lineEdit6.setEnabled(False)
        self.lineEdit6.setFont(QFont('Arial', 11))
        self.lineEdit6.setGeometry(100, 1460, 650, 40)
        self.lineEdit6.setStyleSheet("background-color:white;color:black;")
        self.lineEdit6.setObjectName("lineEdit6")

        self.output_d = QPushButton('Select Folder', self.widget1)
        self.output_d.setGeometry(790,1455,120,50)
        effect = QGraphicsDropShadowEffect(self.output_d)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        self.output_d.setGraphicsEffect(effect)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (13)
        self.output_d.setFont(font)
        self.output_d.setStyleSheet(("QPushButton{background-color:#333335; color: white;border-style: ridge;border-width:0px;border-radius: 3px;border-color: #008CBA;}"))
        self.output_d.clicked.connect(self.output_d_onClick)
        
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget1)
        #self.scroll.setWidget(self.widget2)
        # self.scroll.setGeometry(0,0,1024,768)

        self.buttonWindow4 = QPushButton('Start', self.widget1)
        self.buttonWindow4.setGeometry(440,1570,215,85)
        self.effect = QGraphicsDropShadowEffect(self.buttonWindow4)
        self.effect.setOffset(0, 0)
        self.effect.setBlurRadius(20)
        self.buttonWindow4.setGraphicsEffect(self.effect)
        self.font = QFont()
        self.font.setFamily("Arial")
        self.font.setBold(True)
        self.font.setWeight(50)
        self.font.setPointSize (18)
        self.buttonWindow4.setFont(self.font)
        self.buttonWindow4.setStyleSheet(("QPushButton{background-color:#3C81F8; color: black;border-style: ridge;border-width:1px;border-radius: 10px;border-color: black;}"))
        
        self.buttonWindow4.clicked.connect(self.start)
        
        self.setCentralWidget(self.scroll)
        self.setWindowTitle('Face Swap')

        self.dataView.itemClicked.connect(self.onItemClicked)
        self.dataView1.itemClicked.connect(self.onItemClicked1)
        self.show()
    def onItemClicked(self):
        #global getChildNode
        getSelected = self.dataView.selectedItems()
        #if getSelected:
        baseNode = getSelected[0]
        self.getChildNode = baseNode.text(1)
        print(self.getChildNode)
        

    def add_svideo_onClick(self):
        options=QFileDialog.Options()
        options |=QFileDialog.DontUseNativeDialog
        self.fileNamesrc, _ =QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","MP4 File (*.mp4)",options=options)
        #self.lineEdit5.setText('{}'.format(str(self.fileName3)))
        t=youtube.srcvideo_list
        t.append('{}'.format(str(self.fileNamesrc)))
        print(t,youtube.srcvideo_list)
        QTreeWidgetItem(self.dataView,[str(self.i),t[self.i]])
        self.i=self.i+1
        #for i,x in enumerate(t):
            #print(i,x)
            #QTreeWidgetItem(self.dataView,[str(i),x])
    def del_svideo_onClick(self):
        #for i in reversed(range(self.dataView.childCount())):
            #self.dataView.removeChild(self.dataView.child(i))
        #keydata=self.getChildNode
        #QTreeWidgetItem.removeRow(int(keydata))
        try:
            #if len(self.getChildNode)==0:
                #raise ValueError 
            #self.close()
            #self.destroy()
            #gc.collect() 
            #info.info1=getChildNode
            #self.e.show()
            keydata=self.getChildNode
            print(keydata)
            t=youtube.srcvideo_list
            print(t)
            t.remove(keydata)
            self.i=self.i-1
            #t.append(self.lineEdit1.text())
            #print(t)
            self.dataView.clear()
            for i,x in enumerate(t):
                    #print(i,x)
                    QTreeWidgetItem(self.dataView,[str(i),x])
            # #self.getChildNode=''
        except:
            print("error")
            #self.popup1=popup1(name='      Please select any user to edit!',name2='Okay!')
            #self.popup1.show()
    def onItemClicked1(self):
        #global getChildNode
        getSelected = self.dataView1.selectedItems()
        #if getSelected:
        baseNode = getSelected[0]
        self.getChildNode1 = baseNode.text(1)
        print(self.getChildNode1)
        

    def add_dvideo_onClick(self):
        options=QFileDialog.Options()
        options |=QFileDialog.DontUseNativeDialog
        self.fileNamedst, _ =QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","MP4 File (*.mp4)",options=options)
        t=youtube.dstvideo_list
        t.append('{}'.format(str(self.fileNamedst)))
        print(t,youtube.dstvideo_list)
        QTreeWidgetItem(self.dataView1,[str(self.i1),t[self.i1]])
        self.i1=self.i1+1
        #for i,x in enumerate(t):
            #print(i,x)
            #QTreeWidgetItem(self.dataView,[str(i),x])
    def del_dvideo_onClick(self):
        try:
            keydata=self.getChildNode1
            print(keydata)
            t=youtube.dstvideo_list
            print(t)
            t.remove(keydata)
            self.i1=self.i1-1
            #t.append(self.lineEdit1.text())
            #print(t)
            self.dataView1.clear()
            for i,x in enumerate(t):
                    #print(i,x)
                    QTreeWidgetItem(self.dataView1,[str(i),x])
            # #self.getChildNode=''
        except:
            print("error")
            #self.popup1=popup1(name='      Please select any user to edit!',name2='Okay!')
            #self.popup1.show()

    def srcvideo_b_onClick(self):
        options=QFileDialog.Options()
        options |=QFileDialog.DontUseNativeDialog
        self.fileName1, _ =QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","PNG File (*.png)",options=options)
        self.lineEdit3.setText('{}'.format(str(self.fileName1)))
        print(self.fileName1)

    def dstvideo_b_onClick(self):
        options=QFileDialog.Options()
        options |=QFileDialog.DontUseNativeDialog
        self.fileName2, _ =QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","PNG File (*.png)",options=options)
        self.lineEdit4.setText('{}'.format(str(self.fileName2)))
        print(self.fileName2)
    
    def output_v_onClick(self):
        options=QFileDialog.Options()
        options |=QFileDialog.DontUseNativeDialog
        self.fileName3, _ =QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","MP4 File (*.mp4)",options=options)
        self.lineEdit5.setText('{}'.format(str(self.fileName3)))
        print(self.fileName3)

    def output_d_onClick(self):
        self.fileName4=str(QFileDialog.getExistingDirectory())
        self.lineEdit6.setText('{}'.format(str(self.fileName4)))
        print(self.fileName4)

    def start(self):
        youtube.lineedit3=self.lineEdit3.text()
        youtube.lineedit4=self.lineEdit4.text()
        self.calc = External1()
        self.calc.start()
class External1(QThread):
    def run(self):
        import glob
        import os
        import glob
        from pathlib import Path
        import sys
        import shutil
        dir_path = 'data/processed/'
        #dir_path1='data/processed/model_data_fallon_to_oliver'
        try:
            shutil.rmtree(dir_path)
            #shutil.rmtree(dir_path1)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))
        files = glob.glob('data/videos/*.*', recursive=True)

        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))
        files = glob.glob('data/persons/*.*', recursive=True)
        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))
        do2=''
        for xaa in reversed(youtube.lineedit3):
            if(xaa=="/"):
                break
            do2=do2+xaa
            #print(do2[::-1])
        
        youtube.srcpic_name=(do2[::-1])
        source1 = youtube.lineedit3
        destination1 = "data/persons/"
        try: 
            shutil.copy(source1, destination1)
            print("File copied successfully.") 
        except shutil.SameFileError: 
            print("Source and destination represents the same file.") 

        except IsADirectoryError: 
            print("Destination is a directory.") 
        except PermissionError: 
            print("Permission denied.")  
        except: 
            print("Error occurred while copying file.")
        
        os.rename('data/persons/'+youtube.srcpic_name,'data/persons/fallon.png')
        
        do2=''
        for xaa in reversed(youtube.lineedit4):
            if(xaa=="/"):
                break
            do2=do2+xaa
            #print(do2[::-1])
        
        youtube.dstpic_name=(do2[::-1])
        source1 = youtube.lineedit4
        destination1 = "data/persons/"
        try: 
            shutil.copy(source1, destination1)
            print("File copied successfully.") 
        except shutil.SameFileError: 
            print("Source and destination represents the same file.") 

        except IsADirectoryError: 
            print("Destination is a directory.") 
        except PermissionError: 
            print("Permission denied.")  
        except: 
            print("Error occurred while copying file.")
        
        os.rename('data/persons/'+youtube.dstpic_name,'data/persons/oliver.png')

        t=youtube.srcvideo_list

        for src in t:
            do2=''
            for xaa in reversed(src):
                    if(xaa=="/"):
                        break
                    do2=do2+xaa
            #print(do2[::-1])
            store=youtube.srcvideo_name
            store.append(do2[::-1] )
            print(store)
            #store.rename=       
            source1 = src

            destination1 = "data/videos/"

            # source to destination 
              
            try: 
                #os.system(f'copy {source1} {destination1}')
                shutil.copy(source1, destination1)
                print("File copied successfully.") 
              
            # If source and destination are same 
            except shutil.SameFileError: 
                print("Source and destination represents the same file.") 
              
            # If destination is a directory. 
            except IsADirectoryError: 
                print("Destination is a directory.") 
              
            # If there is any permission issue 
            except PermissionError: 
                print("Permission denied.") 
              
            # For other errors 
            except: 
                print("Error occurred while copying file.")
        t1=youtube.dstvideo_list
        for src in t1:        
            source1 = src
            do2=''
            for xaa in reversed(src):
                        if(xaa=="/"):
                            break
                        do2=do2+xaa
                #print(do2[::-1])
            store=youtube.dstvideo_name
            store.append(do2[::-1] )
            print(store)
            destination1 = "data/videos/"

            # source to destination 
              
            try: 
                #os.system(f'copy {source1} {destination1}')
                shutil.copy(source1, destination1)
                print("File copied successfully.") 
              
            # If source and destination are same 
            except shutil.SameFileError: 
                print("Source and destination represents the same file.") 
              
            # If destination is a directory. 
            except IsADirectoryError: 
                print("Destination is a directory.") 
              
            # If there is any permission issue 
            except PermissionError: 
                print("Permission denied.") 
              
        #     # For other errors 
        #     except: 
        #         print("Error occurred while copying file.")
        faceit = FaceIt('fallon_to_oliver', 'fallon', 'oliver')
        srcstring_list=youtube.srcvideo_name
        for src in srcstring_list:
            faceit.add_video('fallon', src)
        dststring_list=youtube.dstvideo_name
        for dst in dststring_list:
            faceit.add_video('oliver', dst)
        #faceit.add_video('oliver', 'sec_10.mp4')
        

        FaceIt.add_model(faceit)
        faceit.preprocess()
        faceit.train()

class youtube():
    srcvideo_list=[]
    dstvideo_list=[]
    srcvideo_name=[]
    dstvideo_name=[]
    srcpic_name=''
    dstpic_name=''
    lineedit3=''
    lineedit4=''

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()