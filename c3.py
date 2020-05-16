from PyQt5.QtGui import QPixmap,QPainter,QFont,QCursor,QMovie,QTextCursor,QColor,QPen
from PyQt5.QtCore import QThread,QDir, pyqtSignal,QTimer,QTime,Qt,QRect
from PyQt5.QtWidgets import (QPlainTextEdit,QHeaderView,QScroller,QAbstractItemView,QComboBox,QGraphicsDropShadowEffect,QWidget,QMainWindow,QFrame,
  QApplication, QDialog,QProgressBar, QPushButton,QMdiSubWindow,
  QTreeWidget,QLabel,QLineEdit,QTreeWidgetItem,
  QMdiArea,QGraphicsView,QInputDialog, QLineEdit, QFileDialog,QSizePolicy,QHBoxLayout,QScrollArea,QVBoxLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic
import sys


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
        source_label=QLabel("Face Swap Using Youtube Videos",self.widget1)
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
        self.lineEdit1 = QLineEdit(self.widget1)
        self.lineEdit1.setEnabled(True)
        self.lineEdit1.setFont(QFont('Arial', 11))
        self.lineEdit1.setGeometry(100, 213, 650, 40)
        self.lineEdit1.setStyleSheet("background-color:white;color:black;")
        self.lineEdit1.setPlaceholderText("Enter Youtube Video Url")
        self.lineEdit1.setObjectName("lineEdit1")
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
        self.lineEdit2 = QLineEdit(self.widget1)
        self.lineEdit2.setEnabled(True)
        self.lineEdit2.setFont(QFont('Arial', 11))
        self.lineEdit2.setGeometry(100, 653, 650, 40)
        self.lineEdit2.setStyleSheet("background-color:white;color:black;")
        self.lineEdit2.setPlaceholderText("Enter Youtube Video Url")
        self.lineEdit2.setObjectName("lineEdit2")
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
        
        #self.buttonWindow4.clicked.connect(self.buttonWindow4_onClick)
        
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
        
        t=youtube.srcvideo_list
        t.append(self.lineEdit1.text())
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
        
        t=youtube.dstvideo_list
        t.append(self.lineEdit2.text())
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
        pass

class youtube():
    srcvideo_list=[]
    dstvideo_list=[]
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()