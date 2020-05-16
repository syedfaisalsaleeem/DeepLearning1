from PyQt5.QtGui import QPixmap,QPainter,QFont,QCursor,QMovie,QTextCursor,QColor,QPen
from PyQt5.QtCore import QThread,QDir, pyqtSignal,QTimer,QTime,Qt,QRect
from PyQt5.QtWidgets import (QPlainTextEdit,QHeaderView,QScroller,QAbstractItemView,QComboBox,QGraphicsDropShadowEffect,QWidget,QMainWindow,QFrame,
  QApplication, QDialog,QProgressBar, QPushButton,QMdiSubWindow,
  QTreeWidget,QLabel,QLineEdit,QTreeWidgetItem,
  QMdiArea,QGraphicsView,QInputDialog, QLineEdit, QFileDialog,QSizePolicy,QHBoxLayout,QScrollArea,QVBoxLayout)
import sys
import os
from datetime import datetime
#import imageio
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#from skimage.transform import resize
#from IPython.display import HTML
import warnings
#from part_swap import load_checkpoints,load_face_parser,make_video,img_as_ubyte
#import torch
import gc
#from moviepy.editor import VideoFileClip
#from face_alignment.api import FaceAlignment, LandmarksType, NetworkSize
#from face_alignment import FaceDetector
from tqdm import tqdm

import sqlite3
import glob
from pathlib import Path

import shutil
#hiddenimports=['pkg_resources.py2_warn']



class External1(QThread):
  import os
  def convert1(self,seconds):
    hours = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return hours, mins, seconds
  def run(self):
        dir_path = 'workspace2/data_src/'
        dir_path1 = 'workspace2/data_dst/'
        dir_path2 = 'workspace2/model/'
        try:
            shutil.rmtree(dir_path)
            shutil.rmtree(dir_path1)
            shutil.rmtree(dir_path2)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))
        files = glob.glob('workspace2/*.*', recursive=True)

        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))
        try: 
            #os.mkdir("workspace2")
            os.makedirs("workspace2/data_dst/aligned")
            os.makedirs("workspace2/data_src/aligned")
            os.mkdir("workspace2/data_dst/merged")
            os.mkdir("workspace2/data_dst/merged_mask")
            os.mkdir("workspace2/model")
         
        except OSError as error: 
            print(error)
        #os.mkdir("workspace2")
        #os.makedirs("workspace2/data_dst/aligned")
        #os.makedirs("workspace2/data_src/aligned")
        #os.mkdir("workspace2/data_dst/merged")
        #os.mkdir("workspace2/data_dst/merged_mask")
        #os.mkdir("workspace2/model")
        
        clip=VideoFileClip(store.f2)
        video_duration = int(clip.duration)
        hours, mins, secs = self.convert1(video_duration)
        print(mins)
        clip.close()
        if(mins>=1):
            
            if os.path.exists("output.mp4"):
              os.remove("output.mp4")
            else:
              print("The file does not exist")
            myvideo=VideoFileClip(store.f2)
            myvideo1edited=myvideo.subclip(t_start="00:00:00",t_end="00:00:59")
            myvideo1edited.write_videofile('output.mp4')
            #os.system(f"python cropvideo1.py --inp {store.f2}") 
            do_it()
        else:
            #pass
            do_it1()
            #os.system(f"python cropvideo.py --inp {store.f2} --start {store.start}")

        source_image = imageio.imread(store.f1)
        reader = imageio.get_reader('crop.mp4')
        fps = reader.get_meta_data()['fps']
        reader.close()
        driving_video = imageio.mimread('crop.mp4', memtest=False)
        # source_image = imageio.imread(store.f1)
        # driving_video = imageio.mimread(store.f2)

        source_image = resize(source_image, (256, 256))[..., :3]
        driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]
        print('cpu',store.gpu)
        reconstruction_module, segmentation_module = load_checkpoints(config='config/vox-256-sem-10segments.yaml', 
                                                       checkpoint='vox-first-order.pth.tar',
                                                       blend_scale=0.125, first_order_motion_model=True,cpu=store.gpu)

        face_parser = load_face_parser(cpu=store.gpu)


        predictions = make_video(swap_index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], source_image = source_image,
                                 target_video = driving_video, use_source_segmentation=True, segmentation_module=segmentation_module,
                                 reconstruction_module=reconstruction_module, face_parser=face_parser,cpu=store.gpu)
        if os.path.exists('workspace2/data_src.mp4'):
            os.remove('workspace2/data_src.mp4')
        else:
              print("The file does not exist")


        imageio.mimsave('workspace2/data_src.mp4', [img_as_ubyte(frame) for frame in predictions], fps=fps)

        # Python program to explain shutil.copyfile() method  
            
        # importing shutil module  
          
        # Source path 
        source1 = store.f2#jo input lengai high quality mp4
        #time = QTime.currentTime().toString()

        #self.time_label.setText(str(time)+"\n"+store.output)
        #os.rename(store.f2,'data_dst.mp4')  
        # Destination path
        #source1 = store.f2 
        destination1 = "./workspace2/"

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
        os.rename('workspace2/'+store.rename,'workspace2/data_dst.mp4')#jo input lengai high quality mp4
        conn = sqlite3.connect("faisal.db")
        c = conn.cursor() 
        c.execute(f"Update iteration set iter='{store.i}' where key=1")
        conn.commit()
        conn.close()
        #c.close()
        os.system("python main.py videoed extract-video --input-file workspace2/data_src.mp4 --output-dir workspace2/data_src/ --fps 0 --output-ext png")
        os.system("python main.py videoed extract-video --input-file workspace2/data_dst.mp4 --output-dir workspace2/data_dst/ --fps 0 --output-ext png")


        os.system("python main.py extract --input-dir workspace2/data_src --output-dir  workspace2/data_src/aligned --detector s3fd --force-gpu-idxs 0")
        os.system("python main.py extract --input-dir workspace2/data_dst --output-dir  workspace2/data_dst/aligned --detector s3fd --force-gpu-idxs 0")
        #model should be from software SAEHD,SAE,"Quick96", "H128",
        os.system("python main.py train --training-data-src-dir workspace2/data_src/aligned --training-data-dst-dir workspace2/data_dst/aligned --pretraining-data-dir pretrain --model-dir workspace2/model --model SAEHD --silent-start")



        #os.system("python main.py convert --input-dir workspace/data_dst --output-dir workspace/data_dst/merged --aligned-dir workspace/data_dst/aligned --model-dir workspace/model --model SAEHD")
        os.system("python main.py merge --input-dir workspace2/data_dst --output-dir workspace2/data_dst/merged --output-mask-dir workspace2/data_dst/merged_mask --aligned-dir workspace2/data_dst/aligned --model-dir workspace2/model --model SAEHD --force-gpu-idxs 0 ")
        os.system(f"python main.py videoed video-from-sequence --input-dir workspace2/data_dst/merged --output-file {store.f3.strip()+'/'+str(store.f4)+'.mp4'} --reference-file workspace2/data_dst.mp4 --include-audio")

        store.output='Completed..Now you may check the file'
        #imageio.mimsave(opt.result_video, [img_as_ubyte(frame) for frame in predictions], fps=fps)
class popup1(QDialog):
    def __init__(self,name=None,name2=None):
        super().__init__()
        self.title = "App"
        self.name=name
        self.name2=name2
        #self.tablefirsttime=0
        self.InitUI()
    def InitUI(self):
            #a=QFrame()
            #print("start")
            self.setGeometry(237,209,550,350)
            self.setWindowModality(Qt.ApplicationModal)
            self.setWindowFlags(Qt.WindowStaysOnTopHint  | Qt.FramelessWindowHint)
            self.setStyleSheet('background-color:white;border:2px solid black')
            self._gif =QLabel(self)
            self._gif.setPixmap(QPixmap('error.png'))
            self._gif.move(215,30)
            self._gif.setStyleSheet('background-color:white;border:0px solid white')
            label1 = QLabel('Error',self)
            label1.setFont(QFont('Arialbold', 22))
            label1.setStyleSheet('background-color:white;border:0px solid white')
            label1.move(236,130)
            label2 = QLabel(self.name,self)
            label2.setFont(QFont('Arial', 19))
            label2.setStyleSheet('background-color:white;border:0px solid white')
            label2.move(50,170)
            no = QPushButton(self.name2, self)
            no.setGeometry(155,240,240,80)
            no.setFont(QFont('Arial', 21))
            no.setStyleSheet('background-color:#4299ff; color: white')
            no.clicked.connect(self.call_no)
            #self.show()
            #a.show()
    def call_no(self):
        self.close()
        #self.destroy()
        #gc.collect() 


class automaticdeepfake(QMainWindow):
        #def __init__(self, parent=None):
        #super(AnalogGaugeWidget, self).__init__(parent)
    def __init__(self):
       #parent=None
       super().__init__()
       #self.setGeometry(0, 100, 1024, 668)
       self.title = "App"
       self.top = 0
       self.left = 0
       self.width = 1024
       self.height = 768
       #self.setupUi()
       self.InitUI()
       


    def updateTime(self):

        currentDT = datetime.now()


    # def setupUI(self):
    #     if(store.check==True):
    #         self.l.setText("*Your PC contains GPU")
    #     else:
    #        self.l.setText("*Your PC does not contain GPU") 

       
    def InitUI(self):
        #self.setWindowTitle(self.title)
        #self.mdi = QMdiArea()
        #self.setCentralWidget(self.mdi)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint) 
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.mainwidget = QWidget()
        self.scrollArea = QScrollArea(self.mainwidget)
        self.widget = QWidget()
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setStyleSheet('background-color:white;')



        #self.ct.setObjectName("label")
        timer = QTimer(self)
        timer.timeout.connect(self.updateTime)
        timer.start(100)
        #windoww.win=self.mdi
        #mySubwindow=subwindow()
        #self.mdi.addSubWindow(mySubwindow)
        #mySubwindow.close()

        





        self.epf = QLabel("Enter PNG Format Picture",self)
        #self.epf.setFont(QFont('Arial', 18))
        effect = QGraphicsDropShadowEffect(self.epf)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        self.epf.setGraphicsEffect(effect)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (18)
        self.epf.setFont(font)
        self.epf.setStyleSheet(("QLabel{background-color:#4299ff; color: white;padding-left:8px;border-style: ridge;border-width:0px;border-radius: 10px;border-color: #008CBA;}"))
        #self.epf.setStyleSheet('background-color:#4299ff;padding-left:10px;')
        self.epf.setGeometry(30, 67,970,80)

        buttonWindow1 = QPushButton('Select File', self)
        buttonWindow1.setGeometry(890,80,90,50)
        effect = QGraphicsDropShadowEffect(buttonWindow1)
        effect.setOffset(0, 0)
        effect.setBlurRadius(10)
        buttonWindow1.setGraphicsEffect(effect)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (13)
        buttonWindow1.setFont(font)
        buttonWindow1.setStyleSheet(("QPushButton{background-color:#333335; color: white;border-style: ridge;border-width:0px;border-radius: 3px;border-color: #008CBA;}"))
        
        buttonWindow1.clicked.connect(self.buttonWindow1_onClick)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setFont(QFont('Arial', 11))
        self.lineEdit.setGeometry(330, 85, 550, 40)
        self.lineEdit.setStyleSheet("background-color:white;color:black;")
        self.lineEdit.setObjectName("lineEdit")

        



        self.evf = QLabel("High Resolution Mp4 Video",self)
        #self.epf.setFont(QFont('Arial', 18))
        effect = QGraphicsDropShadowEffect(self.evf)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        self.evf.setGraphicsEffect(effect)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (18)
        self.evf.setFont(font)
        self.evf.setStyleSheet(("QLabel{background-color:#4299ff; color: white;padding-left:8px;border-style: ridge;border-width:0px;border-radius: 10px;border-color: #008CBA;}"))
        #self.epf.setStyleSheet('background-color:#4299ff;padding-left:10px;')
        self.evf.setGeometry(30, 167,970,80)

        self.lineEdit1 = QLineEdit(self)
        self.lineEdit1.setEnabled(False)
        self.lineEdit1.setFont(QFont('Arial', 11))
        self.lineEdit1.setGeometry(330, 185, 550, 40)
        self.lineEdit1.setStyleSheet("background-color:white;color:black;")
        self.lineEdit1.setObjectName("lineEdit1")

        buttonWindow2 = QPushButton('Select File', self)
        buttonWindow2.setGeometry(890,180,90,50)
        effect = QGraphicsDropShadowEffect(buttonWindow2)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        buttonWindow2.setGraphicsEffect(effect)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (13)
        buttonWindow2.setFont(font)
        buttonWindow2.setStyleSheet(("QPushButton{background-color:#333335; color: white;border-style: ridge;border-width:0px;border-radius: 3px;border-color: #008CBA;}"))
        
        buttonWindow2.clicked.connect(self.buttonWindow2_onClick)

        self.cp_gp = QLabel("Choose Cpu/Gpu",self)
        #self.epf.setFont(QFont('Arial', 18))
        effect = QGraphicsDropShadowEffect(self.cp_gp)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        self.cp_gp.setGraphicsEffect(effect)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (18)
        self.cp_gp.setFont(font)
        self.cp_gp.setStyleSheet(("QLabel{background-color:#4299ff; color: white;padding-left:8px;border-style: ridge;border-width:0px;border-radius: 10px;border-color: #008CBA;}"))
        #self.epf.setStyleSheet('background-color:#4299ff;padding-left:10px;')
        self.cp_gp.setGeometry(30, 267,970,80)
        
        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(330, 285, 251, 40)
        self.comboBox.setCursor(QCursor(Qt.ArrowCursor))
        self.comboBox.setAcceptDrops(False)
        self.comboBox.setStyleSheet('''QComboBox {     color:black;
    background-color: white;
    border-color: rgba(255,255,255,200);
    border-width: 1px;
    border-style: solid;}'''
"QComboBox:drop-down {width:20px}"


    "QListView { color: black; background-color: white;}")
        self.comboBox.setEditable(False)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("CPU")
        self.comboBox.addItem("GPU")

        self.l = QLabel(self)
        self.l.setFont(QFont('Arial', 13))
        #self.ct.setWeight(QFont(Bold))
        self.l.setStyleSheet('background-color:#4299ff;color:black')

        self.l.setGeometry(590, 280,300,30)

        self.nfi = QLabel("Enter Name of iterations",self)
        #self.epf.setFont(QFont('Arial', 18))
        effect = QGraphicsDropShadowEffect(self.nfi)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        self.nfi.setGraphicsEffect(effect)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (18)
        self.nfi.setFont(font)
        self.nfi.setStyleSheet(("QLabel{background-color:#4299ff; color: white;padding-left:8px;border-style: ridge;border-width:0px;border-radius: 10px;border-color: #008CBA;}"))
        #self.epf.setStyleSheet('background-color:#4299ff;padding-left:10px;')
        self.nfi.setGeometry(30, 367,970,80)
        
        # self.nsf = QLabel("Enter Name Of Savefile",self)
        # self.nsf.setFont(QFont('Arial', 18))
        # #self.ct.setWeight(QFont(Bold))
        # self.nsf.setStyleSheet('background-color:#efeeef;')

        # self.nsf.setGeometry(100, 520,500,30)

        self.lineEditi = QLineEdit(self)
        self.lineEditi.setEnabled(True)
        self.lineEditi.setFont(QFont('Arial', 11))
        self.lineEditi.setGeometry(330, 385, 550, 40)
        self.lineEditi.setStyleSheet("background-color:white;color:black;")
        self.lineEditi.setObjectName("lineEditi")




        self.sf = QLabel("Enter Save Directory",self)
        #self.epf.setFont(QFont('Arial', 18))
        effect = QGraphicsDropShadowEffect(self.sf)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        self.sf.setGraphicsEffect(effect)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (18)
        self.sf.setFont(font)
        self.sf.setStyleSheet(("QLabel{background-color:#4299ff; color: white;padding-left:8px;border-style: ridge;border-width:0px;border-radius: 10px;border-color: #008CBA;}"))
        #self.epf.setStyleSheet('background-color:#4299ff;padding-left:10px;')
        self.sf.setGeometry(30, 467,970,80)

        #self.comboBox.setCurrentText(result_screen.searchkey)

        buttonWindow3 = QPushButton('Select Folder', self)
        buttonWindow3.setGeometry(890,480,100,50)
        effect = QGraphicsDropShadowEffect(buttonWindow3)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        buttonWindow3.setGraphicsEffect(effect)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (13)
        buttonWindow3.setFont(font)
        buttonWindow3.setStyleSheet(("QPushButton{background-color:#333335; color: white;border-style: ridge;border-width:0px;border-radius: 3px;border-color: #008CBA;}"))
        
        buttonWindow3.clicked.connect(self.buttonWindow3_onClick)

        self.lineEdit2 = QLineEdit(self)
        self.lineEdit2.setEnabled(False)
        self.lineEdit2.setFont(QFont('Arial', 11))
        self.lineEdit2.setGeometry(330, 485, 550, 40)
        self.lineEdit2.setStyleSheet("background-color:white;color:black;")
        self.lineEdit2.setObjectName("lineEdit2")

        self.nsf = QLabel("Enter Name of SaveFile",self)
        #self.epf.setFont(QFont('Arial', 18))
        effect = QGraphicsDropShadowEffect(self.nsf)
        effect.setOffset(0, 0)
        effect.setBlurRadius(20)
        self.nsf.setGraphicsEffect(effect)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (18)
        self.nsf.setFont(font)
        self.nsf.setStyleSheet(("QLabel{background-color:#4299ff; color: white;padding-left:8px;border-style: ridge;border-width:0px;border-radius: 10px;border-color: #008CBA;}"))
        #self.epf.setStyleSheet('background-color:#4299ff;padding-left:10px;')
        self.nsf.setGeometry(30, 567,970,80)
        
        # self.nsf = QLabel("Enter Name Of Savefile",self)
        # self.nsf.setFont(QFont('Arial', 18))
        # #self.ct.setWeight(QFont(Bold))
        # self.nsf.setStyleSheet('background-color:#efeeef;')

        # self.nsf.setGeometry(100, 520,500,30)

        self.lineEdit3 = QLineEdit(self)
        self.lineEdit3.setEnabled(True)
        self.lineEdit3.setFont(QFont('Arial', 11))
        self.lineEdit3.setGeometry(330, 585, 550, 40)
        self.lineEdit3.setStyleSheet("background-color:white;color:black;")
        self.lineEdit3.setObjectName("lineEdit3")
        
        self.scrollArea.setGeometry(QRect(0, 0, 1024, 768))
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        #self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setEnabled(True)
        #layout = QVBoxLayout(self)
        #layout.addWidget(self.scrollArea)
        #self.scrollArea.setWidget(self.widget)
        
        self.buttonWindow4 = QPushButton('Start', self.scrollArea)
        self.buttonWindow4.setGeometry(440,870,215,85)
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
        self.buttonWindow4.setStyleSheet(("QPushButton{background-color:#4299ff; color: black;border-style: ridge;border-width:0px;border-radius: 10px;border-color: #008CBA;}"))
        
        self.buttonWindow4.clicked.connect(self.buttonWindow4_onClick)
        


        self.setCentralWidget(self.mainwidget)
        self.show()
    def setupUi(self):
        #automaticdeepfake.setObjectName("Interface")
        #Interface.resize(1152, 1009)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMouseTracking(False)
        #icon = QtGui.QIcon()        

        #self.horizontalLayout = QHBoxLayout()
        #self.horizontalLayout.setObjectName("horizontalLayout")

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(QRect(0, 0, 1024, 768))
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setEnabled(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        #self.horizontalLayout.addWidget(self.scrollArea)

        #centralWidget = QWidgets.QWidget()
        #centralWidget.setObjectName("centralWidget")
        #centralWidget.setLayout(self.horizontalLayout)

        #self.setCentralWidget(centralWidget)
    def bb_onClick(self):
        self.close()
        self.destroy()
        gc.collect()
        self.sub=maingui()
        self.sub.show()

    def buttonWindow1_onClick(self):
        options=QFileDialog.Options()
        options |=QFileDialog.DontUseNativeDialog
        self.fileName1, _ =QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","PNG File (*.png)",options=options)
        self.lineEdit.setText('{}'.format(str(self.fileName1)))
        print(self.fileName1)
        #import subprocess
        #output=subprocess.getoutput("ls -l")
        #print(output)

    def buttonWindow2_onClick(self):
        options=QFileDialog.Options()
        options |=QFileDialog.DontUseNativeDialog
        self.fileName2, _ =QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","MP4 File (*.mp4)",options=options)
        self.lineEdit1.setText('{}'.format(str(self.fileName2)))
        print(self.fileName2)
        #import subprocess
        #output=subprocess.getoutput("ls -l")
        #print(output)
    def buttonWindow3_onClick(self):
        self.fileName3=str(QFileDialog.getExistingDirectory())
        #options |=QFileDialog.DontUseNativeDialog
        #fileName, _ =QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);",options=options)
        self.lineEdit2.setText('{}'.format(str(self.fileName3)))
        print(self.fileName3)
        #import subprocess
        #output=subprocess.getoutput("ls -l")
        #print(output)
    def buttonWindow4_onClick(self):
        try:
            if(len(self.lineEdit.text())!=0 and len(self.lineEditi.text())!=0  and len(self.lineEdit1.text())!=0 and len(self.lineEdit2.text())!=0 and len(self.lineEdit3.text())!=0):
                    print("not error")
                    #self.close()
                    store.f1=self.lineEdit.text()
                    store.f2=self.lineEdit1.text()
                    store.f3=self.lineEdit2.text()
                    store.f4=self.lineEdit3.text()
                    store.i=self.lineEditi.text()
                    gettext=self.comboBox.currentText()
                    store.gettext=gettext
                    print(gettext)
                    lw=len(store.f2)
                    do2=''
                    for xaa in reversed(store.f2):
                        if(xaa=="/"):
                            break
                        do2=do2+xaa
                    print(do2[::-1])
                    store.rename=do2[::-1]
                    try:
                        store.i=int(self.lineEditi.text())
                    except:
                        print("gen")
                        raise ValueError
                    if(store.gettext=="GPU" and store.check==False):
                        #print("error")  
                        self.popup1=popup1(name='      Your PC does not contain GPU!',name2='Okay!')
                        self.popup1.show()

                    else:
                        store.output='''Please wait.. it could take time to finish\n
donot close the window until it is completed'''
                            #print(store.gettext)
                        if(store.gettext=='GPU'):
                                store.gpu=False
                                #print(store.gpu,'this is working')d
                        else:
                                store.gpu=True

                        #self.mna=subwindowadf()
                        #dself.mna.show()

            else:
                print("error")
                #print(type(self.lineEditi.text()))
                self.popup1=popup1(name='      Please fill all the entry fields!',name2='Okay!')
                self.popup1.show()
        except ValueError:
            self.popup1=popup1(name='      Please enter numeric value in iterations!',name2='Okay!')
            self.popup1.show()
        except:
            print("error")
            #print(type(self.lineEditi.text()))
            self.popup1=popup1(name='      Please fill all the entry fields!',name2='Okay!')
            self.popup1.show()



class store():
    f1='11'
    f2=''
    f3=''
    f4=''
    output='''Please wait.. it could take time to finish\n
donot close the window until it is completed'''
    check=""
    gettext=""
    start=''
    gpu=True
    i=0
    rename=''
class subwindowadf(QWidget):

    def __init__(self):
       super().__init__()
       self.title = "App"
       self.top = 0
       self.left = 0
       self.width = 1024
       self.height = 768
       self.one=0
       self.one1=0
       self.InitUI()



    def updateTime(self):
        time = QTime.currentTime().toString()

        self.time_label.setText(str(time)+"\n"+store.output)
        if(store.output=='Completed..Now you may check the file'):
            self.calc.terminate()



       
    def InitUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setStyleSheet('background-color:white;')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        self.time_label = QLabel(self)
        self.time_label.setFont(QFont('Arial', 20,16))
        self.time_label.setStyleSheet('background-color:#efeeef;')
        self.time_label.setGeometry(30, 158,650,450)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(100)

        #print(store.f1,store.f2,store.f3,store.f4)
        #self.output=subprocess.getoutput("python creating1.py")
        
        
        
        

        self.show()
        self.calc = External1()
        self.calc.start()




if __name__ == '__main__':
    def main():
        app = QApplication(sys.argv)
        # y=torch.cuda.is_available()
        # print(y)
        # store.check=y
        # if(y==False):
        #     store.start='cpu'
        # else:
        #     store.start='gpu'
        w = automaticdeepfake()
        w.show()
        sys.exit(app.exec_())

    main()
