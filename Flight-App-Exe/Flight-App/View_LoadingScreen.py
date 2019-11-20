import sys, os
from PyQt5 import QtCore as qtc, QtWidgets as qtw, QtGui as qtg
from PhoneController import PhoneControl
from OpenCVThreadedController import DroneTracker
import time

class LoadingWindow(qtw.QWidget):
    """
    The view for the loading page that is shown when the user presses the "Stop Tracking" button on the tracking window page.

    :ivar __btnHome: The class property for the 'Return to Home' button.
    """

    # Initialize signals. Use for switching between views.
    sigReturnHome = qtc.pyqtSignal()
    sigTestReport = qtc.pyqtSignal()
    sigTransferFootage = qtc.pyqtSignal()

    def __init__(self):
        """
        Class Constructor
        """
        qtw.QWidget.__init__(self)
        self.setFixedSize(550, 550)
        self.initView()

    def initView(self) -> None:
        """
        Sets up the view and lays out all of the components.

        :return: None
        """
        self.setWindowTitle('Loading Screen')

        # Set the title label
        title = self.setTitle()
        self.__lblStatus = self.setSubtitle()

        # Set up loading icon
        loadingIcon = self.setupLoadingIcon()

        self.__btnTestTransfer = qtw.QPushButton("Transfer Video Footage for Analysis")
        self.__btnTestTransfer.clicked.connect(self.signalTransferFootage)

        # Initialize and attach functionality to view report button
        # TODO: For testing purposes only.
        #  Remove button btnTestReport, function signalTestReport, signal sigTestReport, and associated
        #  mapping in Controller class once the functionality is implemented to automatically load report view after
        #  analysis.
        self.__btnTestReport = qtw.QPushButton("Test Report View")
        self.BtnTestReport.clicked.connect(self.signalTestReport)

        # Initialize and attach functionality to home button
        self.__btnHome = qtw.QPushButton('Cancel Analysis and Return to Home')
        self.BtnHome.clicked.connect(self.returnHome)

        # Layout all of the above elements on a vertical layout
        vLayout = qtw.QVBoxLayout()
        vLayout.addWidget(title)
        vLayout.addWidget(self.LblStatus)
        vLayout.addWidget(loadingIcon)
        # vLayout.addWidget(self.__btnTestReport)
        vLayout.addWidget(self.__btnTestTransfer)
        vLayout.addWidget(self.__btnHome)

        # Attach the layout to the screen
        self.setLayout(vLayout)
        self.show()

    def returnHome(self) -> None:
        """
        Sends a signal to the main controller that the Cancel and Return to Home button was pushed.

        :return: none
        """
        self.sigReturnHome.emit()

    def signalTransferFootage(self) -> None:
        """
        Sends a signal to the main controller that the button to transfer footage was pressed.

        :return: none
        """
        self.__lblStatus.setText("File is downloading...")
        qtg.QGuiApplication.processEvents()
        msgBox = qtw.QMessageBox()
        msgBox.setText(
            "Please wait while the footage is transferred.")
        msgBox.exec()
        self.sigTransferFootage.emit()

    def signalTestReport(self) -> None:
        """
        Sends a signal to the main controller that the Test Report button was pushed.
        NOTE: ONLY USED FOR TESTING PURPOSES

        :return: none
        """
        self.sigTestReport.emit()

    def setTitle(self) -> qtw.QLabel:
        """
        Sets up the title with the application title on top and the name of the screen just below it.

        :return: Layout with the application title and screen title labels
        """
        lblTitle = qtw.QLabel("UAS Performance Tracker")
        lblTitle.setFont(qtg.QFont("Helvetica Neue", 36, qtg.QFont.Bold))
        lblTitle.setAlignment(qtc.Qt.AlignCenter)

        return lblTitle

    def setSubtitle(self) -> qtw.QLabel:
        """
        Sets up the subtitle label.

        :return: The subtitle label
        """
        lblStatus = qtw.QLabel("Click button below to initiate transferring of footage.")
        lblStatus.setFont(qtg.QFont("Helvetica Neue", 16))
        lblStatus.setAlignment(qtc.Qt.AlignCenter)

        return lblStatus

    def setupLoadingIcon(self) -> qtw.QLabel:
        """
        Used for configuring the loading icon on the loading screen.
        Loading icon is a gif, so QMovie is used to animate the icon.

        :return: The icon containing the loading label.
        """
        label = qtw.QLabel()
        movie = qtg.QMovie('resources/loading2.gif')
        label.setMovie(movie)
        label.setAlignment(qtc.Qt.AlignCenter)
        label.show()
        movie.start()

        return label

    # region to make label
    @property
    def LblStatus(self) -> qtw.QLabel:
        """
        Getter property for the timer label. We need to attach a QTimer to it so it can count the time the
        application has been tracking the drone.

        :return: The timer label
        """
        return self.__lblStatus

    @LblStatus.setter
    def set_LblStatus(self, lbl: qtw.QLabel) -> None:
        """
        Setter for the LblTimer property.
        :param lbl: The label we want to replace the current one with.

        :return: None
        """
        self.__lblStatus = lbl

    @LblStatus.deleter
    def del_LblStatus(self) -> None:
        """
        Deleter for the timer label.

        :return: None
        """
        del self.__lblStatus
    # end region

    # region > Properties for the buttons so we can attach functionality to them in child classes
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
    def BtnTestReport(self) -> qtw.QPushButton:
        """
        The test report for the view. Is used to switch to the test report screen.

        :return: The reference to the test report button.
        """
        return self.__btnTestReport

    @BtnTestReport.setter
    def set_BtnTestReport(self, btn: qtw.QPushButton) -> None:
        """
        Setter for the test report button.

        :param btn: A Qt QPushButton we want to replace the test report button with.
        :return: None
        """
        self.__btnTestReport = btn

    @BtnTestReport.deleter
    def del_BtnTestReport(self) -> None:
        """
        Deleter for the test report button. Never call this.

        :return: None
        """
        del self.__btnTestReport

    # endregion