import sys
from PyQt5 import QtCore as qtc, QtWidgets as qtw, QtGui as qtg
from Controllers.PhoneController import PhoneControl
# from Controllers.RPIController import RPIController
import signal
from contextlib import contextmanager

class VerifySetupWindow(qtw.QWidget):
    """
    The view for the verify setup page that is shown when the user presses the "Verify Setup" button on the home page.

    :ivar __btnPhoneSync: The class property for the 'Phone Sync' button.
    :ivar __btnTestLight: The class property for the 'Test Light' button.
    :ivar __btnTestFull: The class property for the 'Test Full Setup' button.
    :ivar __btnCheck: The class property for the 'Check Status' button.
    :ivar __btnHome: The class property for the 'Return to Home' button.
    """

    # Initialize signals. Use for switching between views.
    sigReturnHome = qtc.pyqtSignal()
    sigGoodToFly = qtc.pyqtSignal()

    # Initalize status checkers
    phoneSync = False
    lightSync = False
    fullSetup = False

    def __init__(self, phoneControl: PhoneControl) -> None:
        """
        Class constructor.

        :param phoneControl: The PhoneController.PhoneControl Object that is used to send/recieve signals to and from the phone.
        """
        qtw.QWidget.__init__(self)
        self.setFixedSize(550, 550)
        self.phoneControl = phoneControl
        # self.rpiControl = rpiControl
        self.initView()

    def initView(self) -> None:
        """
        Sets up the view and lays out all of the components.

        :return: None
        """
        # Set window title
        self.setWindowTitle('Verify Setup Screen')

        # Set the title label
        title = self.setTitle()
        logo = self.setupPicture()

        # Initialize check status and home buttons
        self.__btnCheck = qtw.QPushButton('Check Setup Status')
        self.__btnHome = qtw.QPushButton('Return to Home')
        statusUpdateButtons = self.setButtonLayout()

        # Attach functionality to buttons
        self.BtnHome.clicked.connect(self.returnHome)
        self.BtnCheck.clicked.connect(self.checkStatus)
        self.BtnPhoneSync.clicked.connect(self.syncPhone)
        #self.BtnTestLight.clicked.connect(self.testLight)
        self.BtnTestFull.clicked.connect(self.testFull)

        # Spacer to make the view more pleasing
        verticalSpacer = qtw.QSpacerItem(20, 40, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
        verticalSpacer2 = qtw.QSpacerItem(20, 40, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)

        # Layout all of the above elements on a vertical layout
        vLayout = qtw.QVBoxLayout()
        vLayout.addLayout(title)
        vLayout.addSpacerItem(verticalSpacer)
        vLayout.addWidget(logo)
        vLayout.addSpacerItem(verticalSpacer2)
        vLayout.addLayout(statusUpdateButtons)  # layout the buttons
        vLayout.addWidget(self.__btnCheck)
        vLayout.addWidget(self.__btnHome)

        # Attach the layout to the screen
        self.setLayout(vLayout)

    def syncPhone(self) -> None:
        """
        Runs phone sync test.

        :return: None
        """
        try:
            self.phoneControl.sync()
            msgBox = qtw.QMessageBox()
            msgBox.setText(
                "Phones synced!")
            msgBox.exec()
            self.phoneSync = True
        except Exception as e:
            msgBox = qtw.QMessageBox()
            msgBox.setText(str(e))
            msgBox.exec()
            self.phoneSync = False

    def testLight(self) -> None:
        """
        Runs light test.

        :return: None
        """
        try:
            # self.rpiControl.flash()
            self.lightSync = True
        except Exception as e:
            msgBox = qtw.QMessageBox()
            msgBox.setText(str(e))
            msgBox.exec()
            self.lightSync = False

    def testFull(self) -> None:
        """
        Runs full system test.

        :return: None
        """
        #if self.lightSync is True and self.phoneControl is True:
        self.fullSetup = True
        #else:
        #    self.fullSetup = False

        if self.fullSetup is True:
            self.sigGoodToFly.emit()
            msgBox = qtw.QMessageBox()
            msgBox.setText(
                "<center><h1>Setup confirmed!</h1></center>\n<center><br><h2>You are ready to fly!</h2></center>")
            msgBox.exec()
        else:
            msgBox = qtw.QMessageBox()
            msgBox.setText(
                "<center><h1>Stop!</h1></center>\n<center><h2>Setup has not been verified!</h2></center>\n"
                "<center><br>Please go back to the startup screen and click the Verify Status button. "
                "Go through the setup process and verify that the performance tracker is set up properly.</center>")
            msgBox.exec()

    def returnHome(self) -> None:
        """
        Sends a signal to the main controller that the Return Home button was pushed.

        :return: none
        """
        self.sigReturnHome.emit()

    def setTitle(self) -> qtw.QVBoxLayout:
        """
        Sets up the title with the application title on top and the name of the screen just below it.
        :return: Layout with the application title and screen title labels
        """
        lblTitle = qtw.QLabel("UAS Performance Tracker")
        lblTitle.setFont(qtg.QFont("Helvetica Neue", 36, qtg.QFont.Bold))
        lblTitle.setAlignment(qtc.Qt.AlignCenter)

        lblTitle2 = qtw.QLabel('Verify Setup')
        lblTitle2.setFont(qtg.QFont("Helvetica Neue", 24, qtg.QFont.Bold))
        lblTitle2.setAlignment(qtc.Qt.AlignCenter)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(lblTitle)
        vbox.addWidget(lblTitle2)

        return vbox

    def setButtonLayout(self) -> qtw.QHBoxLayout:
        """
        Lays out the 'Phone Sync', 'Test Light' and 'Test Full Setup' buttons into a horizontal layout to be
        put on screen.

        :return: The horizontal layout containing the 3 buttons
        """
        self.__btnPhoneSync = qtw.QPushButton('Phone Sync')
        #self.__btnTestLight = qtw.QPushButton('Test Light')
        self.__btnTestFull = qtw.QPushButton('Test Full Setup')

        buttonBox = qtw.QHBoxLayout()
        buttonBox.addWidget(self.__btnPhoneSync)
        #buttonBox.addWidget(self.__btnTestLight)
        buttonBox.addWidget(self.__btnTestFull)

        return buttonBox

    def checkStatus(self) -> None:
        """
         Shows the status of the system setup.

         :return: None
         """
        if self.phoneSync is False:
            phoneStatus = "Phone Status: Not synced\n"
        else:
            phoneStatus = "Phone Status: Synced\n"
        '''
        if self.lightSync is False:
            lightStatus = "Light Status: Not synced\n"
        else:
            lightStatus = "Light Status: Synced\n"
        '''
        if self.fullSetup is False:
            fullSetupStatus = "Full setup: Not synced\n"
        else:
            fullSetupStatus = "Full setup: Synced\n"

        msgBox = qtw.QMessageBox()
        msgBox.setText(
            phoneStatus + fullSetupStatus)
        msgBox.exec()

    def setupPicture(self) -> qtw.QLabel:
        """
        Used for configuring the display for the logo on the screen.

        :return: Returns the label that contains our logo so it can be put on the main panel.
        """
        label = qtw.QLabel()
        pixmap = qtg.QPixmap('../resources/DroneLogo.png')
        pixmap2 = pixmap.scaled(512, 512, qtc.Qt.KeepAspectRatio)
        label.setPixmap(pixmap2)
        label.setAlignment(qtc.Qt.AlignCenter)
        label.show()

        return label

    # region > Properties for the buttons so we can attach functionality to them in child classes

    @property
    def BtnPhoneSync(self) -> qtw.QPushButton:
        """
        The phone sync button so we can attach functionality to it later on.

        :return: The reference to the phoneSync button
        """
        return self.__btnPhoneSync

    @BtnPhoneSync.setter
    def set_BtnPhoneSync(self, btn: qtw.QPushButton) -> None:
        """
        Setter for the phone sync button.

        :param btn: The button we want to replace the current one with
        :return: None
        """
        self.__btnPhoneSync = btn

    @BtnPhoneSync.deleter
    def del_BtnPhoneSync(self) -> None:
        """
        Deleter for the phone sync button

        :return: None
        """
        del self.__btnPhoneSync

    @property
    def BtnTestLight(self) -> qtw.QPushButton:
        """
        The test light button so we can attach functionality to it later on.

        :return: None
        """
        return self.__btnTestLight

    @BtnTestLight.setter
    def set_BtnTestLight(self, btn: qtw.QPushButton) -> None:
        """
        The setter for the test light button.

        :param btn: A Qt QPushButton we want to replace the start button with.
        :return: None
        """
        self.__btnTestLight = btn

    @BtnTestLight.deleter
    def del_BtnTestLight(self) -> None:
        """
        Deleter for the test light button. Never call this.

        :return: None
        """
        del self.__btnTestLight

    @property
    def BtnTestFull(self) -> qtw.QPushButton:
        """
        The test full setup button for the view so we can attach functionality to it later on.
        Is used to import past flight files.

        :return: None
        """
        return self.__btnTestFull

    @BtnTestFull.setter
    def set_BtnTestFull(self, btn: qtw.QPushButton) -> None:
        """
        Setter for the test full setup button.

        :param btn: A Qt QPushButton we want to replace the test full setup button with.
        :return: None
        """
        self.__btnTestFull = btn

    @BtnTestFull.deleter
    def del_BtnTestFull(self) -> None:
        """
        Deleter for the test full setup button. Never call this.

        :return: None
        """
        del self.__btnTestFull

    @property
    def BtnHome(self) -> qtw.QPushButton:
        """
        The home for the view. Is used to return to home screen.

        :return: None
        """
        return self.__btnHome

    @BtnHome.setter
    def set_BtnHome(self, btn: qtw.QPushButton) -> None:
        """
        Setter for the home button.

        :param btn: A Qt QPushButton we want to replace the home button with.
        :return: None
        """
        self.__btnHome = btn

    @BtnHome.deleter
    def del_BtnHome(self) -> None:
        """
        Deleter for the home button. Never call this.

        :return: None
        """
        del self.__btnHome

    @property
    def BtnCheck(self) -> qtw.QPushButton:
        """
        The check status button for the view so we can attach functionality to it later on.
        Is used to check the status of the set up procedures.

        :return: None
        """
        return self.__btnCheck

    @BtnCheck.setter
    def set_BtnCheck(self, btn: qtw.QPushButton) -> None:
        """
        Setter for the check status button.

        :param btn: A Qt QPushButton we want to replace the check status button with.
        :return: None
        """
        self.__btnCheck = btn

    @BtnCheck.deleter
    def del_BtnCheck(self) -> None:
        """
        Deleter for the check status button. Never call this.

        :return: None
        """
        del self.__btnCheck

    # endregion