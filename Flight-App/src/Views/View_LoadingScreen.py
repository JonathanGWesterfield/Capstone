import sys
from PyQt5 import QtCore as qtc, QtWidgets as qtw, QtGui as qtg

class LoadingWindow(qtw.QWidget):
    """
    The view for the loading page that is shown when the user presses the "Stop Tracking" button on the tracking window page.

    :ivar __btnHome: The class property for the 'Return to Home' button.
    """

    # Initialize signals. Use for switching between views.
    sigReturnHome = qtc.pyqtSignal()
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
        self.setWindowTitle('Loading Screen')

        # Set the title label
        title = self.setTitle()

        # Set up loading icon
        loadingIcon = self.setupLoadingIcon()

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
        vLayout.addLayout(title)
        vLayout.addWidget(loadingIcon)
        vLayout.addWidget(self.__btnTestReport)
        vLayout.addWidget(self.__btnHome)

        # Attach the layout to the screen
        self.setLayout(vLayout)

    def returnHome(self):
        """
        Sends a signal to the main controller that the Cancel and Return to Home button was pushed.
        :return: none
        """
        self.sigReturnHome.emit()

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

        lblLoading = qtw.QLabel("Please wait while the flight is analyzed...")
        lblLoading.setFont(qtg.QFont("Helvetica Neue", 16))
        lblLoading.setAlignment(qtc.Qt.AlignCenter)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(lblTitle)
        vbox.addWidget(lblLoading)

        return vbox

    def setupLoadingIcon(self):
        """
        Used for configuring the loading icon on the loading screen.
        Loading icon is a gif, so QMovie is used to animate the icon.
        :return: None
        """
        label = qtw.QLabel()
        movie = qtg.QMovie('../resources/loading2.gif')
        label.setMovie(movie)
        label.setAlignment(qtc.Qt.AlignCenter)
        label.show()
        movie.start()

        return label

    # region > Properties for the buttons so we can attach functionality to them in child classes
    @property
    def BtnHome(self) -> qtw.QPushButton:
        """
        The home for the view. Is used to return to home screen.
        :return: None
        """
        return self.__btnHome

    @BtnHome.setter
    def set_BtnHome(self, btn: qtw.QPushButton):
        """
        Setter for the home button.
        :param btn: A Qt QPushButton we want to replace the home button with.
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
    def BtnTestReport(self) -> qtw.QPushButton:
        """
        The test report for the view. Is used to switch to the test report screen.
        :return: None
        """
        return self.__btnTestReport

    @BtnTestReport.setter
    def set_BtnTestReport(self, btn: qtw.QPushButton):
        """
        Setter for the test report button.
        :param btn: A Qt QPushButton we want to replace the test report button with.
        :return: None
        """
        self.__btnTestReport = btn

    @BtnTestReport.deleter
    def del_BtnTestReport(self):
        """
        Deleter for the test report button. Never call this.
        :return: None
        """
        del self.__btnTestReport

    # endregion