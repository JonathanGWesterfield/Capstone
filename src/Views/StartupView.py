#!/usr/bin/env python

import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

from src.Views.BaseUI import BaseView


class StartupView(BaseView):
    """
    The view for the startup page that is shown when the user starts the application. Inherits from the BaseView Class.
    We need to attach functionality to the controls on this view in the child "controller" class.

    :ivar __btnTestConfig: The class property for the 'TestConfig' button. Allows us to attach functionality to it.
    :ivar __btnStart: The class property for the 'Start' button. Allows us to attach functionality to it.
    :ivar __btnImport: The class property for the 'Import' button. Allows us to attach functionality to it.
    """

    def __init__(self):
        """
        Class constructor. Makes a call to the Base class
        """
        super().__init__()
        self.app = qtw.QApplication([])
        self.initUi()


    def initUi(self):
        """
        Sets up the view and lays out all of the components. Need to attach functionality to it in a
        :return:
        """
        lblTitle = qtw.QLabel(self.get_appName())
        lblTitle.setFont(self.Font)
        lblTitle.setAlignment(qtc.Qt.AlignCenter)

        vLayout = qtw.QVBoxLayout()
        vLayout.addWidget(lblTitle)

        logo = self.setupPicture()
        vLayout.addWidget(logo)

        self.setupButtons()
        vLayout.addLayout(self.buttonBox)

        self.window = qtw.QWidget()
        self.window.setLayout(vLayout)


    def setupButtons(self):
        self.__btnTestConfig = qtw.QPushButton('Verify Camera Setup')
        self.__btnStart = qtw.QPushButton('Start Tracking')
        self.__btnImport = qtw.QPushButton('Import Previous Flight')

        self.buttonBox = qtw.QHBoxLayout()
        self.buttonBox.addWidget(self.__btnTestConfig)
        self.buttonBox.addWidget(self.__btnStart)
        self.buttonBox.addWidget(self.__btnImport)

    def setupPicture(self):
        """
        Used for configuring the display for the logo on the startup screen.
        :return: None
        """
        logo = qtw.QLabel()
        logo.setAlignment(qtc.Qt.AlignCenter)
        logo.setPixmap(qtg.QPixmap("src/resources/Tamu_Seal.png"))
        # picture.(self.picture.width(), self.picture.height())

        # TODO: FIX THIS, THE PICTURE DOESN'T SHOW UP FOR SOME REASON AND NO ERROR IS THROWN
        return logo


    def showWindow(self):
        """
        Takes all of the elements from the view and displays the window.
        :return: None
        """
        self.window.show()
        self.app.exec_()

    # Getters and setters for the buttons to attach functionality to
    @property
    def btnTestConfig(self)->qtw.QPushButton:
        """
        The testConfig button so we can attach functionality to it later on.
        :return: The reference to the testConfig button
        """
        return self.__btnTestConfig

    @btnTestConfig.setter
    def set_btnTestConfig(self, btn: qtw.QPushButton):
        self.__btnTestConfig = btn

    @btnTestConfig.deleter
    def del_btnTestConfig(self):
        del self.__btnTestConfig

    @property
    def btnStart(self)->qtw.QPushButton:
        """
        The Start button for the startup view. Need to access this to attach functionality to the button in a
        child controller class.
        :return: None
        """
        return self.__btnStart

    @btnStart.setter
    def set_btnStart(self, btn: qtw.QPushButton):
        """
        The setter for the start button.
        :param btn: A Qt QPushButton we want to replace the start button with.
        :return: None
        """
        self.__btnStart = btn

    @btnStart.deleter
    def del_btnStart(self):
        """
        Deleter for the start button. Never call this.
        :return: None
        """
        del self.__btnStart

    @property
    def btnImport(self)->qtw.QPushButton:
        """
        The Import button for the view. Need to access this to attach functionality to the button in a
        child controller class. Is used to import past flight files.
        :return: None
        """
        return self.__btnImport

    @btnImport.setter
    def set_btnImport(self, btn: qtw.QPushButton):
        """
        Setter for the import button.
        :param btn: A Qt QPushButton we want to replace the import button with.
        :return: None
        """
        self.__btnImport = btn

    @btnImport.deleter
    def del_btnImport(self):
        """
        Deleter for the import button. Never call this.
        :return: None
        """
        del self.__btnImport


    # Creating the class properties for the buttons. Allows to easily attach functionality to them
    btnTestConfig = property(btnTestConfig, set_btnTestConfig, del_btnTestConfig)
    btnStart = property(btnStart, set_btnStart, del_btnStart)
    btnImport = property(btnImport, set_btnImport, del_btnImport)


ui = StartupView()
ui.showWindow()