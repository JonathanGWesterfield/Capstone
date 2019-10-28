import sys
from PyQt5 import QtCore as qtc, QtWidgets as qtw, QtGui as qtg

class StartupWindow(qtw.QWidget):
    """
    The view for the home Startup page that is shown when the user opens the application.

    :ivar __btnVerifySetup: The class property for the 'Verify Setup' button. Allows us to attach functionality to it.
    :ivar __btnStart: The class property for the 'Start Tracking' button. Allows us to attach functionality to it.
    :ivar __btnImport: The class property for the 'Import Previous Flight' button. Allows us to attach functionality to it.
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
        self.initView()

    def initView(self):
        """
        Sets up the view and lays out all of the components.
        :return: None
        """
        self.setWindowTitle('Startup Window')

        # Set the labels for title and team members
        lblTitle = self.setTitle("UAS Performance Tracker")
        lblTeam = self.setTeamMembers()

        # Set the app logo
        logo = self.setupPicture()

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
        vLayout.addWidget(lblTitle)
        vLayout.addWidget(logo)
        vLayout.addLayout(btnLayout)
        vLayout.addWidget(self.__btnTestReport)
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

    def setTitle(self, text) -> qtw.QLabel:
        """
        Sets up the title label for the window
        :return: Title of the application
        """
        lblTitle = qtw.QLabel(text)
        lblTitle.setFont(qtg.QFont("Helvetica Neue", 24, qtg.QFont.Bold))
        lblTitle.setAlignment(qtc.Qt.AlignCenter)

        return lblTitle

    def setTeamMembers(self) -> qtw.QLabel:
        """
        Sets up the team members label for the window
        :return: Team members label of the application
        """
        lblTeam = qtw.QLabel("Jonathan Westerfield, Hayley Eckert, Donald Elrod, Ismael Rodriguez, Ariana Boroujerdi")
        lblTeam.setFont(qtg.QFont("Helvetica Neue", 14))
        lblTeam.setAlignment(qtc.Qt.AlignCenter)

        return lblTeam

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