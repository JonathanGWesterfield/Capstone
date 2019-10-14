#!/usr/bin/env python

import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

class StartupUI:

    def __init__(self):
        self.app = qtw.QApplication([])
        self.setupWindow();


    def setupWindow(self):
        self.label = qtw.QLabel('UAS Performance Tracker')
        self.label.setFont(qtg.QFont("Helvetica Neue", 36, qtg.QFont.Bold))
        self.label.setAlignment(qtc.Qt.AlignCenter)

        self.layout = qtw.QVBoxLayout()
        self.layout.addWidget(self.label)

        # self.setupPicture()
        # self.layout.addWidget(self.picture)

        self.setupButtons()
        self.layout.addLayout(self.buttonBox)

        self.window = qtw.QWidget()
        self.window.setLayout(self.layout)


    def setupButtons(self):
        self.btnTestConfig = qtw.QPushButton('Verify Camera Setup')
        self.btnStart = qtw.QPushButton('Start Tracking')
        self.btnImport = qtw.QPushButton('Import Previous Flight')

        self.buttonBox = qtw.QHBoxLayout()
        self.buttonBox.addWidget(self.btnTestConfig)
        self.buttonBox.addWidget(self.btnStart)
        self.buttonBox.addWidget(self.btnImport)

    def setupPicture(self):
        self.picture = qtw.QLabel()
        pixmap = qtw.QGraphicsPixmapItem('../resources/Tamu_Seal.png')
        self.picture.setPixmap(pixmap)
        self.picture.resize(pixmap.width(), pixmap.height())


    def showWindow(self):
        self.window.show()
        self.app.exec_()

ui = StartupUI()
ui.showWindow()