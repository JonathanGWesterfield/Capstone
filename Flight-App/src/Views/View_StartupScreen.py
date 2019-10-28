import sys
from PyQt5 import QtCore as qtc, QtWidgets as qtw, QtGui as qtg

class StartupWindow(qtw.QWidget):
    """
    The view for the home Startup page that is shown when the user opens the application.

    :ivar __btnVerifySetup: The class property for the 'Verify Setup' button.
    :ivar __btnStart: The class property for the 'Start Tracking' button.
    :ivar __btnImport: The class property for the 'Import Previous Flight' button.
    """

    # Initialize signals. Use for switching between views.
    sigVerifySetup = qtc.pyqtSignal()
    sigStartTracking = qtc.pyqtSignal()
    sigImportFlight = qtc.pyqtSignal()
    sigTestReport = qtc.pyqtSignal()

    def __init__(self):
        """
        Class Constructor
        """
        qtw.QWidget.__init__(self)
        self.setFixedSize(550, 550)
        self.initView()

    def initView(self):
        """
        Sets up the view and lays out all of the components.
        :return: None
        """
        self.setWindowTitle('Home Screen')

        # Set the labels for title and team members
        lblTitle = self.setTitle()
        lblTeam = self.setTeamMembers()

        # Set the app logo
        logo = self.setupPicture()

        # Set up the Texas A&M icon
        icon = self.setupAMLogo()

        # Initialize buttons and attach functionality
        btnLayout = self.setButtonLayout()
        # TODO: Remove button btnTestReport, function signalTestReport, signal sigTestReport, and associated
        #  mapping in Controller class once the functionality is implemented to automatically load report view after
        #  analysis. For now, used for testing purposes.
        self.__btnTestReport = qtw.QPushButton("Test Report View")
        self.BtnVerifySetup.clicked.connect(self.signalVerifySetup)
        self.BtnStart.clicked.connect(self.signalStartTracking)
        self.BtnImport.clicked.connect(self.signalImportFlight)
        self.__btnTestReport.clicked.connect(self.signalTestReport)

        # Layout all of the above elements on a vertical layout
        vLayout = qtw.QVBoxLayout()
        vLayout.addLayout(lblTitle)
        vLayout.addWidget(logo)
        vLayout.addLayout(btnLayout)
        vLayout.addWidget(self.__btnTestReport)
        vLayout.addWidget(icon)
        vLayout.addWidget(lblTeam)

        # Attach the layout to the screen
        self.setLayout(vLayout)

    def signalVerifySetup(self):
        """
        Sends a signal to the main controller that the Verify Setup button was pushed.
        :return: none
        """
        self.sigVerifySetup.emit()

    def signalStartTracking(self):
        """
        Sends a signal to the main controller that the Start Tracking button was pushed.
        :return: none
        """
        self.sigStartTracking.emit()

    def signalImportFlight(self):
        """
        Sends a signal to the main controller that the Import Previous Flight button was pushed.
        :return: none
        """
        self.sigImportFlight.emit()

    def signalTestReport(self):
        """
        Sends a signal to the main controller that the Test Report button was pushed.
        NOTE: ONLY USED FOR TESTING PURPOSES
        :return: none
        """
        self.sigTestReport.emit()

    def setTitle(self) -> qtw.QVBoxLayout:
        """
        Sets up the title with the application title on top and the name of the screen just below it.
        :return: Layout with the application title and screen title labels
        """
        lblTitle = qtw.QLabel("UAS Performance Tracker")
        lblTitle.setFont(qtg.QFont("Helvetica Neue", 36, qtg.QFont.Bold))
        lblTitle.setAlignment(qtc.Qt.AlignCenter)

        lblTitle2 = qtw.QLabel('Home Screen')
        lblTitle2.setFont(qtg.QFont("Helvetica Neue", 24, qtg.QFont.Bold))
        lblTitle2.setAlignment(qtc.Qt.AlignCenter)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(lblTitle)
        vbox.addWidget(lblTitle2)

        return vbox

    def setTeamMembers(self) -> qtw.QVBoxLayout:
        """
        Sets up the team members label for the window
        :return: Team members label of the application
        """
        lblTeam1 = qtw.QLabel("Team members:\nJonathan Westerfield, Hayley Eckert, Donald Elrod, \nIsmael Rodriguez, Ariana Boroujerdi")
        lblTeam1.setFont(qtg.QFont("Helvetica Neue", 14))
        lblTeam1.setAlignment(qtc.Qt.AlignCenter)
        lblTeam1.setWordWrap(True)

        return lblTeam1

    def setButtonLayout(self) -> qtw.QHBoxLayout:
        """
        Lays out the 'Test Config', 'Start' and 'Import' buttons into a horizontal layout to be
        put on screen.
        :return: The horizontal layout containing the 3 buttons
        """
        self.__btnVerifySetup = qtw.QPushButton('Verify Setup')
        self.__btnStart = qtw.QPushButton('Start Tracking')
        self.__btnImport = qtw.QPushButton('Import Previous Flight')

        buttonBox = qtw.QHBoxLayout()
        buttonBox.addWidget(self.__btnVerifySetup)
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

    def setupAMLogo(self):
        """
        Used for configuring the display for the A&M logo on the startup screen.
        :return: None
        """
        label = qtw.QLabel()
        pixmap = qtg.QPixmap('../resources/Tamu_Seal.png')
        pixmap2 = pixmap.scaled(128, 128, qtc.Qt.KeepAspectRatio)
        label.setPixmap(pixmap2)
        label.setAlignment(qtc.Qt.AlignCenter)
        label.show()

        return label

    # region > Properties for the buttons so we can attach functionality to them in child classes

    @property
    def BtnVerifySetup(self) -> qtw.QPushButton:
        """
        Getter for the verifySetup button. Use to attach functionality.
        :return: The reference to the verifySetup button
        """
        return self.__btnVerifySetup

    @BtnVerifySetup.setter
    def set_BtnVerifySetup(self, btn: qtw.QPushButton):
        """
        Setter for the verify setup button.
        :param btn: The button we want to replace the current one with
        :return: None
        """
        self.__btnVerifySetup = btn

    @BtnVerifySetup.deleter
    def del_BtnVerifySetup(self):
        """
        Deleter for the verify setup button
        :return: None
        """
        del self.__btnVerifySetup

    @property
    def BtnStart(self) -> qtw.QPushButton:
        """
        Getter for the startTracking button. Use to attach functionality.
        :return: None
        """
        return self.__btnStart

    @BtnStart.setter
    def set_BtnStart(self, btn: qtw.QPushButton):
        """
        The setter for the startTracking button.
        :param btn: A Qt QPushButton we want to replace the start button with.
        :return: None
        """
        self.__btnStart = btn

    @BtnStart.deleter
    def del_BtnStart(self):
        """
        Deleter for the startTracking button. Never call this.
        :return: None
        """
        del self.__btnStart

    @property
    def BtnImport(self) -> qtw.QPushButton:
        """
        Getter for the Import Previous Flight button. Is used to import past flight files. Use to attach functionality.
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

    # endregion