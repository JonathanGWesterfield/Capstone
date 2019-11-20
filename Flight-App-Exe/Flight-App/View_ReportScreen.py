import sys
from PyQt5 import QtCore as qtc, QtWidgets as qtw, QtGui as qtg
import Graph
import Graph
import ExportFile
import ImportFile
import datetime as dt
import json
import os

class ReportWindow(qtw.QWidget):
    """
    The view for the report page that is shown when the user opens the application.

    :ivar __btnExport: The class property for the 'Export Results' button.
    :ivar __btnFlyAgain: The class property for the 'Fly Again' button.
    :ivar __btnHome: The class property for the 'Return to Home' button.
    :ivar __btnViewGraphVelocity: The class property for the 'View Flight Path' button.
    :ivar __btnViewGraphNoVelocity: The class property for the 'View Flight Path with Velocity Changes' button.
    :var __btnViewInstructions: The class property for the 'View Flight Instructions' button.
    """

    # Initialize signals. Use for switching between views.
    sigStartTracking = qtc.pyqtSignal()
    sigReturnHome = qtc.pyqtSignal()
    def __init__(self, pilotName: str, instructorName: str, flightInstructions: str, previousFlight: str,
                 usingPreviousFlight: bool, flightData: dict) -> None:
        """
        Class Constructor
        """
        qtw.QWidget.__init__(self)

        # Initiate the view
        self.initView(pilotName, instructorName, flightInstructions, previousFlight, usingPreviousFlight, flightData)

        # Format window
        self.setFixedSize(550, 700)

    def initView(self, pilotName: str, instructorName: str, flightInstructions: str, previousFlight: str,
                 usingPreviousFlight: bool, flightData: dict) -> None:
        """
        Sets up the view and lays out all of the components.

        :param pilotName: String containing pilot name
        :param instructorName: String containing instructor name
        :param flightInstructions: String containing flight instructions.
        :param previousFlight: String containing path to flight data. Should be .flight file if usingPreviousFlight is true, or blank if usingPreviousFlight is false.
        :param usingPreviousFlight: Boolean denoting if the report should be populated from the same file or a different one.
        :param flightDict: Dictionary containing flight data. Should be empty if usingPreviousFlight is true.
        :return: None
        """
        # Analyze the flight
        self.flightDict = {}
        if usingPreviousFlight is False:
            self.flightDict = self.analyzeFlight(flightData)
            self.flightDict["pilotName"] = pilotName
            self.flightDict["instructorName"] = instructorName
            self.flightDict["flightInstr"] = flightInstructions
            self.flightDict["flightDate"] = dt.datetime.now().strftime('%m-%d-%Y-%H:%M:%S')
        else:
            self.flightDict = ImportFile.importData(previousFlight)

        # Load in information for sliders
        self.minTime = 0
        self.maxTime = 0
        self.minRangeTime = 0
        self.maxRangeTime = 0
        self.MAXVAL = self.flightDict["flightLength"]

        self.sliderMin = 0
        self.sliderMax = self.MAXVAL

        # Set up the title, flight information table, and statistics table.
        self.setWindowTitle('Report Screen')
        titleLayout = self.setupTitle()
        flInfoLayout = self.setupFlightInfo()
        statistics = self.createStatisticsTable()

        # Set up more labels
        graph_label = self.setSubTitle("Flight Graph")
        slider_label = qtw.QLabel("Select time range to view: ")
        slider_label.setAlignment(qtc.Qt.AlignLeft)

        # Initialize buttons.
        self.__btnViewGraphNoVelocity = qtw.QPushButton('View Flight Path')
        self.__btnViewGraphVelocity = qtw.QPushButton('View Flight Path with Velocity Changes')
        btnLayout = self.setButtonLayout()

        # Attach functionality to buttons.
        self.BtnExport.clicked.connect(self.signalExportResults)
        self.BtnFlyAgain.clicked.connect(self.signalStartTracking)
        self.BtnHome.clicked.connect(self.signalReturnHome)
        self.BtnViewGraphNoVelocity.clicked.connect(lambda *args: self.setupGraph(self.flightDict, False))
        self.BtnViewGraphVelocity.clicked.connect(lambda *args: self.setupGraph(self.flightDict, True))

        # Add a slider
        slider = self.setupSlider()

        # Create a grid layout for all elements except the title.
        gridLayout = qtw.QGridLayout()
        gridLayout.addLayout(flInfoLayout, 0, 0)
        gridLayout.addWidget(statistics, 1, 0)
        gridLayout.addWidget(graph_label, 2, 0)
        gridLayout.addWidget(slider_label, 3, 0)
        gridLayout.addLayout(slider, 4, 0)
        gridLayout.addWidget(self.BtnViewGraphNoVelocity, 5, 0)
        gridLayout.addWidget(self.BtnViewGraphVelocity, 6, 0)
        gridLayout.addLayout(btnLayout, 7, 0)  # layout the buttons

        # Layout all of the above elements on a vertical layout
        vLayout = qtw.QVBoxLayout()
        vLayout.addLayout(titleLayout)
        vLayout.addLayout(gridLayout)

        # Attach the layout to the screen
        self.setLayout(vLayout)

    def signalExportResults(self) -> None:
        """
        Sends a signal to the main controller that the Export Results button was pushed.

        :return: none
        """
        # Save flight results to .flight file.
        outFolder = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/drone-tracker/Flights/')
        outPath = outFolder + self.flightDict["pilotName"] + '_' + self.flightDict["flightDate"] + '.flight'
        with open(outPath, 'w') as outfile:
            json.dump(self.flightDict, outfile)
        # Show message box saying that exporting was completed.
        msgBox = qtw.QMessageBox()
        msgBox.setText(
            "Results exported!")
        msgBox.exec()

    def signalStartTracking(self) -> None:
        """
        Sends a signal to the main controller that the Fly Again button was pushed.

        :return: none
        """
        self.sigStartTracking.emit()

    def signalReturnHome(self) -> None:
        """
        Sends a signal to the main controller that the Return Home button was pushed.

        :return: none
        """
        self.sigReturnHome.emit()

    def setupTitle(self) -> qtw.QVBoxLayout:
        """
        Sets up the title with the application title on top and the name of the screen just below it.

        :return: Layout with the application title and screen title labels
        """
        lblTitle = qtw.QLabel("UAS Performance Tracker")
        lblTitle.setFont(qtg.QFont("Helvetica Neue", 36, qtg.QFont.Bold))
        lblTitle.setAlignment(qtc.Qt.AlignCenter)

        lblScreenTitle = qtw.QLabel('Flight Report')
        lblScreenTitle.setFont(qtg.QFont("Helvetica Neue", 24, qtg.QFont.Bold))
        lblScreenTitle.setAlignment(qtc.Qt.AlignCenter)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(lblTitle)
        vbox.addWidget(lblScreenTitle)

        return vbox

    def setSubTitle(self, text) -> qtw.QLabel:
        """
        Sets up a subtitle label for the window

        :param text: String as name for label
        :return: Subtitle label
        """
        lblTitle = qtw.QLabel(text)
        lblTitle.setFont(qtg.QFont("Helvetica Neue", 16, qtg.QFont.Bold))
        lblTitle.setAlignment(qtc.Qt.AlignLeft)

        return lblTitle

    def setupFlightInfo(self) -> qtw.QGridLayout:
        """
        Sets up the flight info (pilot, instructor, date, length, and smoothness score) in a grid.

        :return: Grid layout of the flight information
        """
        # Setup all labels with default values for testing and detecting errors in the controls
        self.__lblPilot = qtw.QLabel(self.flightDict["pilotName"])
        self.__lblInstructor = qtw.QLabel(self.flightDict["instructorName"])
        self.__lblFlDate = qtw.QLabel(self.flightDict["flightDate"])
        self.__lblFlLength = qtw.QLabel(str(self.flightDict["flightLength"]))

        grid = qtw.QGridLayout()
        flightInfoTitle = self.setSubTitle('Flight Information')
        grid.addWidget(flightInfoTitle, 0, 0)
        grid.addWidget(qtw.QLabel('Pilot: '), 1, 0)
        grid.addWidget(self.LblPilot, 1, 1)
        grid.addWidget(qtw.QLabel('Instructor: '), 2, 0)
        grid.addWidget(self.LblInstructor, 2, 1)
        grid.addWidget(qtw.QLabel('Flight Date: '), 3, 0)
        grid.addWidget(self.LblFlightDate, 3, 1)
        grid.addWidget(qtw.QLabel('Flight Length: '), 4, 0)
        grid.addWidget(self.LblFlightLength, 4, 1)

        statisticsInfoTitle = self.setSubTitle("Statistics")
        grid.addWidget(statisticsInfoTitle, 5, 0)

        return grid

    def setupGraph(self, flightData: dict, displayVelocity: bool) -> None:
        """
         Sets up the 3d plot for viewing upon click of button. displayVelocity is a boolean denoting if the graph should
         display colored segments for velocity.

         :param flightData: Dictionary of flight data
         :param displayVelocity: Bool denoting if velocity should be plotted or not.
         :return: None
         """
        # Generate and show graph
        minTime = self.MAXVAL - (self.startSlider.value() / 100)
        maxTime = self.endSlider.value() / 100
        print("Min slider value:" + str(minTime))
        print("Max slider value:" + str(maxTime))

        if maxTime <= minTime:
            msgBox = qtw.QMessageBox()
            msgBox.setText(
                "Start time must be less than end time!\n Please reselect a time range using the sliders.")
            msgBox.exec()
        else:
            fig = Graph.generateGraph(flightData, displayVelocity, minTime, maxTime)

            # Define manager so figure can be viewed upon button click
            new_manager = fig.canvas.manager
            new_manager.canvas.figure = fig
            fig.set_canvas(new_manager.canvas)

            # Show the figure
            fig.show()

    def setButtonLayout(self) -> qtw.QHBoxLayout:
        """
        Lays out the 'Export Results', 'Fly Again' and 'Import Previous Flight' buttons into a horizontal layout to be
        put on screen.

        :return: The horizontal layout containing the 3 buttons
        """
        self.__btnExport = qtw.QPushButton('Export Results')
        self.__btnFlyAgain = qtw.QPushButton('Fly Again')
        self.__btnHome = qtw.QPushButton('Return to Home')

        buttonBox = qtw.QHBoxLayout()
        buttonBox.addWidget(self.__btnExport)
        buttonBox.addWidget(self.__btnFlyAgain)
        buttonBox.addWidget(self.__btnHome)

        return buttonBox

    def showWindow(self) -> None:
        """
        Takes all of the elements from the view and displays the window.

        :return: None
        """
        self.window.show()

    def createStatisticsTable(self) -> qtw.QTableWidget:
        """
        Creates a table containing flight statistics.

        :return: QTableWidget containing flight statistics.
        """
        # Create table
        self.tableWidget = qtw.QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['Property', 'Value'])
        header = self.tableWidget.horizontalHeader()
        self.tableWidget.setFixedHeight(144)
        header.setSectionResizeMode(0, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(1, qtw.QHeaderView.Stretch)

        self.tableWidget.setItem(0, 0, qtw.QTableWidgetItem("Smoothness Metric as Jerk (m/s^3)"))
        self.tableWidget.setItem(0, 1, qtw.QTableWidgetItem(str(round(self.flightDict["smoothness"], 2))))
        self.tableWidget.setItem(1, 0, qtw.QTableWidgetItem("Average Velocity Change (m/s)"))
        self.tableWidget.setItem(1, 1, qtw.QTableWidgetItem(str(round(2*self.flightDict["avgVel"], 2))))
        self.tableWidget.setItem(2, 0, qtw.QTableWidgetItem("Minimum Velocity Change (m/s)"))
        self.tableWidget.setItem(2, 1, qtw.QTableWidgetItem(str(round(2*self.flightDict["minVel"], 2))))
        self.tableWidget.setItem(3, 0, qtw.QTableWidgetItem("Maximum Velocity Change (m/s)"))
        self.tableWidget.setItem(3, 1, qtw.QTableWidgetItem(str(round(2*self.flightDict["maxVel"], 2))))

        # Make non-editable
        self.tableWidget.setEditTriggers(qtw.QTableWidget.NoEditTriggers)

        return self.tableWidget

    def analyzeFlight(self, flightDict: dict) -> dict:
        """
        Analyzes the flight data to extract coordinates, velocity values, and statistics.

        :param flightDict: Dictionary of flight data, with only coordinates populated.
        :return: Updated dictionary, with legal points and flight statistics included.
        """
        # Check legality of coordinates.
        flightDict = Graph.checkCoordinates(flightDict)

        # Update flightDict to contain velocity
        flightDict1 = Graph.velocityPoints(flightDict)

        # Update flightDict to contain statistics on velocity points
        flightDict2 = Graph.computeVelocityStatistics(flightDict1)

        # Compute smoothness value
        flightDict2["smoothness"] = Graph.log_dimensionless_jerk(flightDict2["velocities"], 0.5)

        return flightDict2

    def setupSlider(self) -> qtw.QVBoxLayout:
        """
        Setups the slider that will be used to adjust the times of the flight path that will be displayed
        on the graph. This lets us control the beginning and ending bounds of the time of the flight
        that we want to view. We have to use 2 sliders. One for the start time and one for the end.
        We originally wanted to make this such that both sliders were on top of each other to make
        it more intuitive, but we ran into a bug that prevented us from doing that.

        :return: A horizontal layout containing both sliders and the labels displaying the time that they represent.
        """
        horizontalLayout0 = qtw.QHBoxLayout()
        horizontalLayout0.setSizeConstraint(qtw.QLayout.SetMinimumSize)
        horizontalLayout0.setContentsMargins(5, 2, 5, 2)
        horizontalLayout0.setSpacing(0)
        horizontalLayout0.setObjectName("horizontalLayout")

        ## Start Slider Widget
        self.startSlider = qtw.QSlider()
        self.startSlider.setMaximum(100 * self.MAXVAL)

        self.startSlider.setMinimumSize(qtc.QSize(100, 5))
        self.startSlider.setMaximumSize(qtc.QSize(16777215, 10))

        font = qtg.QFont()
        font.setKerning(True)

        self.startSlider.setFont(font)
        self.startSlider.setAcceptDrops(False)
        self.startSlider.setAutoFillBackground(False)
        self.startSlider.setInvertedAppearance(True)
        self.startSlider.setOrientation(qtc.Qt.Horizontal)
        self.startSlider.setObjectName("startSlider")
        self.startSlider.setValue(100*self.MAXVAL)
        self.startSlider.valueChanged.connect(self.handleStartSliderValueChange)
        horizontalLayout0.addWidget(self.startSlider)

        horizontalLayout1 = qtw.QHBoxLayout()
        horizontalLayout1.setSizeConstraint(qtw.QLayout.SetMinimumSize)
        horizontalLayout1.setContentsMargins(5, 2, 5, 2)
        horizontalLayout1.setSpacing(0)
        horizontalLayout1.setObjectName("horizontalLayout")

        ## End Slider Widget
        self.endSlider = qtw.QSlider()
        #self.endSlider.setMaximum(100 * self.MAXVAL/2)
        self.endSlider.setMaximum(100 * self.MAXVAL)
        self.endSlider.setMinimumSize(qtc.QSize(100, 5))
        self.endSlider.setMaximumSize(qtc.QSize(16777215, 10))
        self.endSlider.setTracking(True)
        self.endSlider.setOrientation(qtc.Qt.Horizontal)
        self.endSlider.setObjectName("endSlider")
        self.endSlider.setValue(100*self.MAXVAL)
        self.endSlider.valueChanged.connect(self.handleEndSliderValueChange)
        horizontalLayout1.addWidget(self.endSlider)

        # Add minimum and maximum values
        horizontalLayout2 = qtw.QHBoxLayout()
        self.label_minimum = qtw.QLabel("0 s")
        self.label_minimum.setAlignment(qtc.Qt.AlignLeft)
        self.label_maximum = qtw.QLabel(str(self.MAXVAL) + " s")
        self.label_maximum.setAlignment(qtc.Qt.AlignRight)
        horizontalLayout2.addWidget(self.label_minimum)
        horizontalLayout2.addWidget(self.label_maximum)

        # Add current value
        horizontalLayout3 = qtw.QHBoxLayout()
        self.label_current_min_title = qtw.QLabel("Start Time: ")
        self.label_current_min_title.setAlignment(qtc.Qt.AlignLeft)
        self.label_current_min = qtw.QLabel("0")
        self.label_current_min.setAlignment(qtc.Qt.AlignLeft)
        horizontalLayout3.addWidget(self.label_current_min_title)
        horizontalLayout3.addWidget(self.label_current_min)
        horizSpacer = qtw.QSpacerItem(150, 20, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
        self.label_current_max_title = qtw.QLabel("End Time: ")
        self.label_current_max_title.setAlignment(qtc.Qt.AlignRight)
        self.label_current_max = qtw.QLabel(str(self.MAXVAL))
        self.label_current_max.setAlignment(qtc.Qt.AlignRight)
        horizontalLayout3.addSpacerItem(horizSpacer)
        horizontalLayout3.addWidget(self.label_current_max_title)
        horizontalLayout3.addWidget(self.label_current_max)

        vbox = qtw.QVBoxLayout()
        vbox.addLayout(horizontalLayout2)
        vbox.addLayout(horizontalLayout0)
        vbox.addLayout(horizontalLayout1)
        vbox.addLayout(horizontalLayout3)

        qtc.QMetaObject.connectSlotsByName(self)

        return vbox

    @qtc.pyqtSlot(int)
    def handleStartSliderValueChange(self, value) -> None:
        """
        Listener that will updated the start time label when the user moves the start
        time slider.

        :param value: The value that the start slider has been moved to horizontally.
        :return: None
        """
        self.startSlider.setValue(value)
        minTime = self.MAXVAL - (self.startSlider.value() / 100)
        self.label_current_min.setText(str(round(minTime, 2)))
        # print("start " + str(value))

    @qtc.pyqtSlot(int)
    def handleEndSliderValueChange(self, value) -> None:
        """
        Listener that will updated the stop time label when the user moves the stop
        time slider.

        :param value: The value that the stop slider has been moved to horizontally.
        :return: None
        """
        self.endSlider.setValue(value)
        maxTime = self.endSlider.value() / 100
        self.label_current_max.setText(str(round(maxTime, 2)))
        # print("stop " + str(value))

    # region > Report View Properties

    # region > Pilot Label Property

    @property
    def LblPilot(self) -> qtw.QLabel:
        """
        Getter for the Pilot label so we can set who the pilot is for the flight in child class.

        :return: Reference to the pilot label.
        """
        return self.__lblPilot

    @LblPilot.setter
    def set_LblPilot(self, lbl: qtw.QLabel) -> None:
        """
        Setter for the pilot Label.

        :param lbl: The label we want to replace the current one with.
        :return: None
        """
        self.__lblPilot = lbl

    @LblPilot.deleter
    def del_LblPilot(self) -> None:
        """
        Deleter for the pilot label.

        :return: None
        """
        del self.__lblPilot

    # endregion

    # region > Instructor Label Property
    @property
    def LblInstructor(self) -> qtw.QLabel:
        """
        Getter for the instructor label.

        :return: Reference to the instructor label.
        """
        return self.__lblInstructor

    @LblInstructor.setter
    def set_LblInstructor(self, lbl: qtw.QLabel) -> None:
        """
        Setter for the instructor Label.

        :param lbl: The label we want to replace the current one with.
        :return: None
        """
        self.__lblInstructor = lbl

    @LblInstructor.deleter
    def del_LblInstructor(self) -> None:
        """
        Deleter for the instructor label.

        :return: None
        """
        del self.__lblInstructor

    # endregion

    # region > Flight Date Property
    @property
    def LblFlightDate(self) -> qtw.QLabel:
        """
        Getter for the flight date label.

        :return: Reference to the flight date label.
        """
        return self.__lblFlDate

    @LblFlightDate.setter
    def set_LblFlightDate(self, lbl: qtw.QLabel) -> None:
        """
        Setter for the Flight date label.

        :param lbl: The label we want to replace the current one with.
        :return: None
        """
        self.__lblFlDate = lbl

    @LblFlightDate.deleter
    def del_LblFlightDate(self) -> None:
        """
        Deleter for the flight date label.

        :return: None
        """
        del self.__lblFlDate

    # endregion

    # region > Flight Length Label Property
    @property
    def LblFlightLength(self) -> qtw.QLabel:
        """
        Getter for the flight length label.

        :return: Reference to the flight length label.
        """
        return self.__lblFlLength

    @LblFlightLength.setter
    def set_LblFlightLength(self, lbl: qtw.QLabel) -> None:
        """
        Setter for the flight length label.

        :param lbl: The label we want to replace the current one with.
        :return: None
        """
        self.__lblFlLength = lbl

    @LblFlightLength.deleter
    def del_LblFlightLength(self) -> None:
        """
        Deleter for the flight length label.

        :return: None
        """
        del self.__lblFlLength

    # endregion

    # region > Flight Instructions Label Property
    @property
    def LblFlightInstructions(self) -> qtw.QLabel:
        """
        Getter for the flight instructions label.

        :return: Reference to the flight length label.
        """
        return self.__lblFlInstructions

    @LblFlightInstructions.setter
    def set_LblFlightInstructions(self, lbl: qtw.QLabel) -> None:
        """
        Setter for the flight instructions label.

        :param lbl: The label we want to replace the current one with.
        :return: None
        """
        self.__lblFlLengthInstructions = lbl

    @LblFlightInstructions.deleter
    def del_LblFlightInstructions(self) -> None:
        """
        Deleter for the flight length label.

        :return: None
        """
        del self.__lblFlInstructions

    # endregion

    # region > Properties for the buttons

    @property
    def BtnExport(self) -> qtw.QPushButton:
        """
        The export button for the view.

        :return: None
        """
        return self.__btnExport

    @BtnExport.setter
    def set_BtnExport(self, btn: qtw.QPushButton) -> None:
        """
        The setter for the export button.

        :param btn: A Qt QPushButton we want to replace the export button with.
        :return: None
        """
        self.__btnExport = btn

    @BtnExport.deleter
    def del_BtnExport(self) -> None:
        """
        Deleter for the export button. Never call this.

        :return: None
        """
        del self.__btnExport

    @property
    def BtnFlyAgain(self) -> qtw.QPushButton:
        """
        The fly again button for the view.

        :return: None
        """
        return self.__btnFlyAgain

    @BtnFlyAgain.setter
    def set_BtnFlyAgain(self, btn: qtw.QPushButton) -> None:
        """
        Setter for the fly again button.

        :param btn: A Qt QPushButton.
        :return: None
        """
        self.__btnFlyAgain = btn

    @BtnFlyAgain.deleter
    def del_BtnFlyAgain(self) -> None:
        """
        Deleter for the fly again button. Never call this.

        :return: None
        """
        del self.__btnFlyAgain

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

        :param btn: A Qt QPushButton.
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
    def BtnViewGraphVelocity(self) -> qtw.QPushButton:
        """
        The home for the view graph with velocity button.

        :return: None
        """
        return self.__btnViewGraphVelocity

    @BtnViewGraphVelocity.setter
    def set_BtnViewGraphVelocity(self, btn: qtw.QPushButton) -> None:
        """
        Setter for the view graph with velocity button.

        :param btn: A Qt QPushButton.
        :return: None
        """
        self.__btnViewGraphVelocity = btn

    @BtnViewGraphVelocity.deleter
    def del_BtnViewGraphVelocity(self) -> None:
        """
        Deleter for the view graph with velocity button. Never call this.

        :return: None
        """
        del self.__btnViewGraphVelocity

    @property
    def BtnViewGraphNoVelocity(self) -> qtw.QPushButton:
        """
        The home for the view graph without velocity button.

        :return: None
        """
        return self.__btnViewGraphNoVelocity

    @BtnViewGraphNoVelocity.setter
    def set_BtnViewGraphNoVelocity(self, btn: qtw.QPushButton) -> None:
        """
        Setter for the view graph without velocity button.

        :param btn: A Qt QPushButton.
        :return: None
        """
        self.__btnViewGraphNoVelocity = btn

    @BtnViewGraphNoVelocity.deleter
    def del_BtnViewGraphNoVelocity(self) -> None:
        """
        Deleter for the view graph without velocity button. Never call this.

        :return: None
        """
        del self.__btnViewGraphNoVelocity

    # endregion