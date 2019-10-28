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
        self.initView()


    def initView(self):
        """
        Sets up the view and lays out all of the components. Need to attach functionality to it in a
        :return: None
        """

        # Set the title label
        lblTitle = qtw.QLabel(self.get_appName())
        lblTitle.setFont(self.TitleFont)
        lblTitle.setAlignment(qtc.Qt.AlignCenter)

        # Set the app logo
        logo = self.setupPicture()

        # Set the label with the team members
        lblTeam = qtw.QLabel(self.getStrTeamMembers())
        lblTeam.setFont(self.RegularFont)
        lblTeam.setAlignment(qtc.Qt.AlignCenter)

        # Layout all of the above elements on a vertical layout
        vLayout = qtw.QVBoxLayout()
        vLayout.addWidget(lblTitle)
        vLayout.addWidget(logo)
        vLayout.addLayout(self.setButtonLayout()) # layout the buttons
        vLayout.addWidget(lblTeam)

        # Attach the layout to the screen
        self.window = qtw.QWidget()
        self.window.setLayout(vLayout)

    def setButtonLayout(self) -> qtw.QHBoxLayout:
        """
        Lays out the 'Test Config', 'Start' and 'Import' buttons into a horizontal layout to be
        put on screen.
        :return: The horizontal layout containing the 3 buttons
        """
        self.__btnTestConfig = qtw.QPushButton('Verify Camera Setup')
        self.__btnStart = qtw.QPushButton('Start Tracking')
        self.__btnImport = qtw.QPushButton('Import Previous Flight')

        buttonBox = qtw.QHBoxLayout()
        buttonBox.addWidget(self.__btnTestConfig)
        buttonBox.addWidget(self.__btnStart)
        buttonBox.addWidget(self.__btnImport)

        return buttonBox

    def setupPicture(self):
        """
        Used for configuring the display for the logo on the startup screen.
        :return: None
        """
        label = qtw.QLabel()
        pixmap = qtg.QPixmap('../resources/DroneLogo.png')
        pixmap2 = pixmap.scaled(512, 512, qtc.Qt.KeepAspectRatio)
        label.setPixmap(pixmap2)
        label.setAlignment(qtc.Qt.AlignCenter)
        label.show()

        return label


    def showWindow(self):
        """
        Takes all of the elements from the view and displays the window.
        :return: None
        """
        self.window.show()
        self.app.exec_()

    #region > Properties for the buttons so we can attach functionality to them in child classes

    @property
    def BtnTestConfig(self)->qtw.QPushButton:
        """
        The testConfig button so we can attach functionality to it later on.
        :return: The reference to the testConfig button
        """
        return self.__btnTestConfig

    @BtnTestConfig.setter
    def set_BtnTestConfig(self, btn: qtw.QPushButton):
        """
        Setter for the test config button.
        :param btn: The button we want to replace the current one with
        :return: None
        """
        self.__btnTestConfig = btn

    @BtnTestConfig.deleter
    def del_BtnTestConfig(self):
        """
        Deleter for the test config button
        :return: None
        """
        del self.__btnTestConfig

    @property
    def BtnStart(self)->qtw.QPushButton:
        """
        The Start button for the startup view. Need to access this to attach functionality to the button in a
        child controller class.
        :return: None
        """
        return self.__btnStart

    @BtnStart.setter
    def set_BtnStart(self, btn: qtw.QPushButton):
        """
        The setter for the start button.
        :param btn: A Qt QPushButton we want to replace the start button with.
        :return: None
        """
        self.__btnStart = btn

    @BtnStart.deleter
    def del_BtnStart(self):
        """
        Deleter for the start button. Never call this.
        :return: None
        """
        del self.__btnStart

    @property
    def BtnImport(self)->qtw.QPushButton:
        """
        The Import button for the view. Need to access this to attach functionality to the button in a
        child controller class. Is used to import past flight files.
        :return: None
        """
        return self.__btnImport

    @BtnImport.setter
    def set_BtnImport(self, btn: qtw.QPushButton):
        """
        Setter for the import button.
        :param btn: A Qt QPushButton we want to replace the import button with.
        :return: None
        """
        self.__btnImport = btn

    @BtnImport.deleter
    def del_BtnImport(self):
        """
        Deleter for the import button. Never call this.
        :return: None
        """
        del self.__btnImport

    #endregion


ui = StartupView()
ui.showWindow()