#!/usr/bin/env python

import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
from src.Views.BaseUI import BaseView


class VerifySetup(BaseView):
    """
    The view for the verify setup page that is shown when the user presses the "Verify Setup" button on the home page.
    Inherits from the BaseView Class.
    We need to attach functionality to the controls on this view in the child "controller" class.

    :ivar __btnPhoneSync: The class property for the 'Phone Sync' button. Allows us to attach functionality to it.
    :ivar __btnTestLight: The class property for the 'Test Light' button. Allows us to attach functionality to it.
    :ivar __btnTestFull: The class property for the 'Test Full Setup' button. Allows us to attach functionality to it.
    :ivar __btnCheck: The class property for the 'Check Status' button. Allows us to attach functionality to it.
    :ivar __btnHome: The class property for the 'Return to Home' button. Allows us to attach functionality to it.
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
        Sets up the view and lays out all of the components.
        :return: None
        """

        # Set the title label
        lblTitle = qtw.QLabel('Verify Setup')
        lblTitle.setFont(self.TitleFont)
        lblTitle.setAlignment(qtc.Qt.AlignCenter)

        # Set up check status and home buttons
        self.__btnCheck = qtw.QPushButton('Check Setup Status')
        self.__btnHome = qtw.QPushButton('Return to Home')

        # Layout all of the above elements on a vertical layout
        vLayout = qtw.QVBoxLayout()
        vLayout.addWidget(lblTitle)
        vLayout.addLayout(self.setButtonLayout()) # layout the buttons
        vLayout.addWidget(self.__btnCheck)
        vLayout.addWidget(self.__btnHome)

        # Attach the layout to the screen
        self.window = qtw.QWidget()
        self.window.setLayout(vLayout)

    def setButtonLayout(self) -> qtw.QHBoxLayout:
        """
        Lays out the 'Phone Sync', 'Test Light' and 'Test Full Setup' buttons into a horizontal layout to be
        put on screen.
        :return: The horizontal layout containing the 3 buttons
        """
        self.__btnPhoneSync = qtw.QPushButton('Phone Sync')
        self.__btnTestLight = qtw.QPushButton('Test Light')
        self.__btnTestFull = qtw.QPushButton('Test Full Setup')

        buttonBox = qtw.QHBoxLayout()
        buttonBox.addWidget(self.__btnPhoneSync)
        buttonBox.addWidget(self.__btnTestLight)
        buttonBox.addWidget(self.__btnTestFull)

        return buttonBox

    def showWindow(self):
        """
        Takes all of the elements from the view and displays the window.
        :return: None
        """
        self.window.show()
        self.app.exec_()

    #region > Properties for the buttons so we can attach functionality to them in child classes

    @property
    def BtnPhoneSync(self)->qtw.QPushButton:
        """
        The phone sync button so we can attach functionality to it later on.
        :return: The reference to the phoneSync button
        """
        return self.__btnPhoneSync

    @BtnPhoneSync.setter
    def set_BtnPhoneSync(self, btn: qtw.QPushButton):
        """
        Setter for the phone sync button.
        :param btn: The button we want to replace the current one with
        :return: None
        """
        self.__btnPhoneSync = btn

    @BtnPhoneSync.deleter
    def del_BtnPhoneSync(self):
        """
        Deleter for the test config button
        :return: None
        """
        del self.__btnPhoneSync

    @property
    def BtnTestLight(self)->qtw.QPushButton:
        """
        The test light button for the view. Need to access this to attach functionality to the button in a
        child controller class.
        :return: None
        """
        return self.__btnTestLight

    @BtnTestLight.setter
    def set_BtnTestLight(self, btn: qtw.QPushButton):
        """
        The setter for the test light button.
        :param btn: A Qt QPushButton we want to replace the start button with.
        :return: None
        """
        self.__btnTestLight = btn

    @BtnTestLight.deleter
    def del_BtnTestLight(self):
        """
        Deleter for the test light button. Never call this.
        :return: None
        """
        del self.__btnTestLight

    @property
    def BtnTestFull(self)->qtw.QPushButton:
        """
        The test full setup button for the view. Need to access this to attach functionality to the button in a
        child controller class. Is used to import past flight files.
        :return: None
        """
        return self.__btnTestFull

    @BtnTestFull.setter
    def set_BtnTestFull(self, btn: qtw.QPushButton):
        """
        Setter for the test full setup button.
        :param btn: A Qt QPushButton we want to replace the import button with.
        :return: None
        """
        self.__btnTestFull = btn

    @BtnTestFull.deleter
    def del_BtnTestFull(self):
        """
        Deleter for the test full setup button. Never call this.
        :return: None
        """
        del self.__btnTestFull

    @property
    def BtnHome(self)->qtw.QPushButton:
        """
        The home for the view. Need to access this to attach functionality to the button in a
        child controller class. Is used to return to home screen.
        :return: None
        """
        return self.__btnHome

    @BtnHome.setter
    def set_BtnHome(self, btn: qtw.QPushButton):
        """
        Setter for the home button.
        :param btn: A Qt QPushButton we want to replace the import button with.
        :return: None
        """
        self.__btnHome = btn

    @BtnHome.deleter
    def del_BtnHome(self):
        """
        Deleter for the home button. Never call this.
        :return: None
        """
        del self.__btnHome

    @property
    def BtnCheck(self) -> qtw.QPushButton:
        """
        The check status button for the view. Need to access this to attach functionality to the button in a
        child controller class. Is used to check the status of the set up procedures.
        :return: None
        """
        return self.__btnCheck

    @BtnCheck.setter
    def set_BtnCheck(self, btn: qtw.QPushButton):
        """
        Setter for the check status button.
        :param btn: A Qt QPushButton we want to replace the import button with.
        :return: None
        """
        self.__btnCheck = btn

    @BtnCheck.deleter
    def del_BtnCheck(self):
        """
        Deleter for the check status button. Never call this.
        :return: None
        """
        del self.__btnCheck

    #endregion


ui = VerifySetup()
ui.showWindow()