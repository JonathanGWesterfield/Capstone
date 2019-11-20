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
    sigImportFlight = qtc.pyqtSignal(str)

    def __init__(self, flightModeEnabled: bool) -> None:
        """
        Class Constructor
        """
        qtw.QWidget.__init__(self)
        self.setFixedSize(550, 550)
        self.flightModeEnabled = flightModeEnabled
        self.initView()

    def initView(self) -> None:
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
        self.BtnVerifySetup.clicked.connect(self.signalVerifySetup)
        self.BtnImport.clicked.connect(self.signalImportFlight)
        if self.flightModeEnabled is True:
            self.BtnStart.clicked.connect(self.signalStartTracking)

        # Layout all of the above elements on a vertical layout
        vLayout = qtw.QVBoxLayout()
        vLayout.addLayout(lblTitle)
        vLayout.addWidget(logo)
        vLayout.addLayout(btnLayout)
        vLayout.addWidget(icon)
        vLayout.addWidget(lblTeam)

        # Attach the layout to the screen
        self.setLayout(vLayout)

    def signalVerifySetup(self) -> None:
        """
        Sends a signal to the main controller that the Verify Setup button was pushed.

        :return: none
        """
        self.sigVerifySetup.emit()

    def signalStartTracking(self) -> None:
        """
        Sends a signal to the main controller that the Start Tracking button was pushed.

        :return: none
        """
        self.sigStartTracking.emit()

    def signalImportFlight(self) -> None:
        """
        Calls function to allow user to select a file for import.
        Sends a signal to the main controller that the Import Previous Flight button was pushed.

        :return: None.
        """
        fileName = self.openFileNameDialog()
        self.sigImportFlight.emit(fileName)

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
        lblTeam1 = qtw.QLabel("Team members:\nJonathan Westerfield, Hayley Eckert, Donald Elrod, \nIsmael Rodriguez")
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

        if self.flightModeEnabled is False:
            palette = qtg.QPalette()
            palette.setColor(qtg.QPalette.ButtonText, qtc.Qt.red)
            self.__btnStart.setPalette(palette)
            self.__btnStart.update()

        buttonBox = qtw.QHBoxLayout()
        buttonBox.addWidget(self.__btnVerifySetup)
        buttonBox.addWidget(self.__btnStart)
        buttonBox.addWidget(self.__btnImport)

        return buttonBox

    def setupPicture(self) -> None:
        """
        Used for configuring the display for the logo on the startup screen.

        :return: None
        """
        label = qtw.QLabel()
        pixmap = qtg.QPixmap('resources/DroneLogo.png')
        pixmap2 = pixmap.scaled(512, 512, qtc.Qt.KeepAspectRatio)
        label.setPixmap(pixmap2)
        label.setAlignment(qtc.Qt.AlignCenter)
        label.show()

        return label

    def setupAMLogo(self) -> None:
        """
        Used for configuring the display for the A&M logo on the startup screen.

        :return: None
        """
        label = qtw.QLabel()
        pixmap = qtg.QPixmap('resources/Tamu_Seal.png')
        pixmap2 = pixmap.scaled(128, 128, qtc.Qt.KeepAspectRatio)
        label.setPixmap(pixmap2)
        label.setAlignment(qtc.Qt.AlignCenter)
        label.show()

        return label

    def openFileNameDialog(self) -> None:
        """
        Allows user to select a .flight file from a file dialog window.

        :return: Path to selected file as a string.
        """
        options = qtw.QFileDialog.Options()
        options |= qtw.QFileDialog.DontUseNativeDialog
        fileName, _ = qtw.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                      "JSON Files (*.flight)", options=options)

        return fileName

    # region > Properties for the buttons so we can attach functionality to them in child classes

    @property
    def BtnVerifySetup(self) -> qtw.QPushButton:
        """
        Getter for the verifySetup button. Use to attach functionality.

        :return: The reference to the verifySetup button
        """
        return self.__btnVerifySetup

    @BtnVerifySetup.setter
    def set_BtnVerifySetup(self, btn: qtw.QPushButton) -> None:
        """
        Setter for the verify setup button.

        :param btn: The button we want to replace the current one with
        :return: None
        """
        self.__btnVerifySetup = btn

    @BtnVerifySetup.deleter
    def del_BtnVerifySetup(self) -> None:
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
    def set_BtnStart(self, btn: qtw.QPushButton) -> None:
        """
        The setter for the startTracking button.

        :param btn: A Qt QPushButton we want to replace the start button with.
        :return: None
        """
        self.__btnStart = btn

    @BtnStart.deleter
    def del_BtnStart(self) -> None:
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
    def set_BtnImport(self, btn: qtw.QPushButton) -> None:
        """
        Setter for the import button.

        :param btn: A Qt QPushButton we want to replace the import button with.
        :return: None
        """
        self.__btnImport = btn

    @BtnImport.deleter
    def del_BtnImport(self) -> None:
        """
        Deleter for the import button. Never call this.

        :return: None
        """
        del self.__btnImport

    # endregion