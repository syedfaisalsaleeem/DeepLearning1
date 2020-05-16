from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow,QGridLayout,QAbstractScrollArea,QSizePolicy)
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

        #self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()
        self.widget.setStyleSheet('background-color:white;')                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.h2Box = QHBoxLayout()
                       # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        #for i in range(1,100):
            #object = QLabel("")
            #object.resize(1024,760)
            #object.setStyleSheet("background-color:white;")
            #self.vbox.addWidget(object)
        self.object3=QPushButton("asdsa",self)
        #object3.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        #self.object3.setMinimumSize(QSize(500,100))
        self.object3.setStyleSheet("background-color:gray;color:black;")

        #self.object.resize(500,500)
        #self.object.move(500,818)
        #self.vbox.addWidget(self.object3)
        #vbox.setColumnStretch(0, 0)
        #vbox.setRowStretch(0, 0)
        #self.vbox.addWidget(self.object,1,0)
        #self.vbox.addWidget(self.object,2,0)

        self.object1=QPushButton("asdsa",self)
        #object1.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        #self.object1.setMinimumSize(QSize(500,100))
        #self.object.setStyleSheet("background-color:gray;color:black;")
        #self.object.resize(500,500)
        #self.object.move(500,818)
        #self.vbox.addWidget(self.object1)
        #self.vbox.addWidget(self.object1,1,1)
        #self.vbox.addWidget(self.object1,2,1)
        #self.widget.setLayout(self.vbox)

        self.object2=QPushButton("asdsa",self)
        #object1.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        #self.object1.setMinimumSize(QSize(500,100))
        #self.object.setStyleSheet("background-color:gray;color:black;")
        #self.object.resize(500,500)
        #self.object.move(500,818)
        #self.vbox.addWidget(self.object2)
        #self.vbox.addWidget(self.object1,1,1)
        #self.vbox.addWidget(self.object1,2,1)
        #self.widget.setLayout(self.vbox)


        # object2=QPushButton("asdsa")
        # object2.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        # #self.object2.setMinimumSize(QSize(500,900))
        # #self.object.setStyleSheet("background-color:gray;color:black;")
        # #self.object.resize(500,500)
        # #self.object.move(500,818)
        # vbox.addWidget(object2,1,2)
        #self.vbox.addWidget(self.object2,2,0)
        #self.vbox.addWidget(self.object2,3,0)
        #self.vbox.setColumnStretch(0, 0)
        # self.object=QPushButton("asdsa",self)
        # self.vbox.addWidget(self.object,0,1,0,0)
        # self.object=QPushButton("asdsa",self)
        # self.vbox.addWidget(self.object,0,2)
        # self.object=QPushButton("asdsa",self)
        # self.vbox.addWidget(self.object,0,3)
        

        #Scroll Area Properties
        #self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        #self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.scroll.setWidgetResizable(True)
        #self.scroll.setWidget(self.object)
        #self.scroll.setWidget(self.widget)
        #self.scroll.setGeometry(0,0,1024,768)
        #self.setCentralWidget(self.scroll)
        self.hbox.addWidget(self.object1)
        self.hbox.addWidget(self.object3)
        self.h2Box.addWidget(self.object1)
        self.h2Box.addWidget(self.object3)
        #self.h2Box.addWidget(self.object1)
        #self.h2Box.addWidget(self.object1)

        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.h2Box)
        self.widget.setLayout(self.vbox)
        self.setCentralWidget(self.widget)
        self.widget.setGeometry(0,0,500,500)
        self.setGeometry(100, 100, 1024, 760)
        # self.widget2 = QWidget()
        # self.widget2.setStyleSheet('background-color:black;')
        # self.widget2.setGeometry(0,0,500,500) 
        self.setWindowTitle('Scroll Area Demonstration')
        self.show()

        return

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()