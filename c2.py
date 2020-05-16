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
        self.initUI()
        #self.__layout()
    

    #def __layout(self):



    

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
        source_label=QLabel("Face Swap On Local Drive Videos",self.widget1)
        source_label.setStyleSheet('background-color:#FCFCFE;')
        source_label.setFont(QFont('Arial', 22))
        source_label.setGeometry(250,113,600,30)
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
        self.epf.setGeometry(50, 203,900,380)
        source_label=QLabel("Add Source Videos",self.widget1)
        source_label.setStyleSheet('background-color:white;')
        source_label.setFont(QFont('Arial', 22))
        source_label.setGeometry(100,213,600,30)
        bb = QPushButton('+', self.widget1)
        bb.setGeometry(850,213,40,40)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (18)
        bb.setFont(font)
        bb.setStyleSheet(("QPushButton{background-color:red; color: black;border-style: ridge;border-width:0px;border-radius: 20px;border-color: white;}"))
        #bb.clicked.connect(self.bb_onClick)

        bb = QPushButton('-', self.widget1)
        bb.setGeometry(800,213,40,40)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (28)
        bb.setFont(font)
        bb.setStyleSheet(("QPushButton{background-color:blue; color: black;border-style: ridge;border-width:0px;border-radius: 20px;border-color: white;}"))
        #bb.clicked.connect(self.bb_onClick
        

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
        self.epf.setGeometry(50, 703,900,380)
        source_label=QLabel("Add Destination Videos",self.widget1)
        source_label.setStyleSheet('background-color:white;')
        source_label.setFont(QFont('Arial', 22))
        source_label.setGeometry(100,713,600,30)
        bb = QPushButton('+', self.widget1)
        bb.setGeometry(850,713,40,40)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (18)
        bb.setFont(font)
        bb.setStyleSheet(("QPushButton{background-color:red; color: black;border-style: ridge;border-width:0px;border-radius: 20px;border-color: white;}"))
        #bb.clicked.connect(self.bb_onClick)

        bb = QPushButton('-', self.widget1)
        bb.setGeometry(800,713,40,40)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(50)
        font.setPointSize (28)
        bb.setFont(font)
        bb.setStyleSheet(("QPushButton{background-color:blue; color: black;border-style: ridge;border-width:0px;border-radius: 20px;border-color: white;}"))
        #bb.clicked.connect(self.bb_onClick
        

        self.dataView = QTreeWidget(self.widget1)
        self.dataView.setRootIsDecorated(False)
        self.dataView.setHeaderLabels(['Ref No','Destination Videos'])
        self.dataView.header().setStyleSheet('padding-top:-2px;background-color:white;font-size:21pt; font-family: Arial;border-width:1px;border-style:outset;border-color:black; ')
        self.dataView.setColumnCount(2)
        self.dataView.setColumnWidth(0,100)
        self.dataView.setColumnWidth(1,100)

        self.dataView.setStyleSheet('background-color:white;color: black;')
        self.dataView.setFont(QFont('Times New Roman', 22))

        self.dataView.setGeometry(100,760,800,265)
        
        source_label=QLabel("Picture of Person In Source Video",self.widget1)
        source_label.setFont(QFont('Arial', 22))
        source_label.setStyleSheet('background-color:#FCFCFE;')
        source_label.setGeometry(100,1113,600,30)
        self.lineEdit1 = QLineEdit(self.widget1)
        self.lineEdit1.setEnabled(False)
        self.lineEdit1.setFont(QFont('Arial', 11))
        self.lineEdit1.setGeometry(100, 1160, 650, 40)
        self.lineEdit1.setStyleSheet("background-color:white;color:black;")
        self.lineEdit1.setObjectName("lineEdit1")

        buttonWindow2 = QPushButton('Select File', self.widget1)
        buttonWindow2.setGeometry(790,1155,120,50)
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
        
        #buttonWindow2.clicked.connect(self.buttonWindow2_onClick)
        source_label=QLabel("Picture of Person In Destination Video",self.widget1)
        source_label.setFont(QFont('Arial', 22))
        source_label.setStyleSheet('background-color:#FCFCFE;')
        source_label.setGeometry(100,1213,600,30)
        self.lineEdit1 = QLineEdit(self.widget1)
        self.lineEdit1.setEnabled(False)
        self.lineEdit1.setFont(QFont('Arial', 11))
        self.lineEdit1.setGeometry(100, 1260, 650, 40)
        self.lineEdit1.setStyleSheet("background-color:white;color:black;")
        self.lineEdit1.setObjectName("lineEdit1")

        buttonWindow2 = QPushButton('Select File', self.widget1)
        buttonWindow2.setGeometry(790,1255,120,50)
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
        

        source_label=QLabel("Output Video in which face is to be replaced",self.widget1)
        source_label.setStyleSheet('background-color:#FCFCFE;')
        source_label.setFont(QFont('Arial', 22))
        source_label.setGeometry(100,1313,600,30)
        self.lineEdit1 = QLineEdit(self.widget1)
        self.lineEdit1.setEnabled(False)
        self.lineEdit1.setFont(QFont('Arial', 11))
        self.lineEdit1.setGeometry(100, 1360, 650, 40)
        self.lineEdit1.setStyleSheet("background-color:white;color:black;")
        self.lineEdit1.setObjectName("lineEdit1")

        buttonWindow2 = QPushButton('Select File', self.widget1)
        buttonWindow2.setGeometry(790,1355,120,50)
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
        

        source_label=QLabel("Output Directory",self.widget1)
        source_label.setStyleSheet('background-color:#FCFCFE;')
        source_label.setFont(QFont('Arial', 22))
        source_label.setGeometry(100,1413,600,30)
        self.lineEdit1 = QLineEdit(self.widget1)
        self.lineEdit1.setEnabled(False)
        self.lineEdit1.setFont(QFont('Arial', 11))
        self.lineEdit1.setGeometry(100, 1460, 650, 40)
        self.lineEdit1.setStyleSheet("background-color:white;color:black;")
        self.lineEdit1.setObjectName("lineEdit1")

        buttonWindow2 = QPushButton('Select Folder', self.widget1)
        buttonWindow2.setGeometry(790,1455,120,50)
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
        self.show()

        return

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()