import sys
from PyQt5 import QtCore as qtc, QtWidgets as qtw, QtGui as qtg
import Graph
import Export.ExportFile
import Export.ImportFile
import datetime as dt

class ReportWindow(qtw.QWidget):
    """
    The view for the report page that is shown when the user opens the application.

    :ivar __btnExport: The class property for the 'Export Results' button.
    :ivar __btnFlyAgain: The class property for the 'Fly Again' button.
    ivar __btnHome: The class property for the 'Return to Home' button.
    :ivar __btnViewGraphVelocity: The class property for the 'View Flight Path' button.
    :ivar __btnViewGraphNoVelocity: The class property for the 'View Flight Path with Velocity Changes' button.
    :var __btnViewInstructions: The class property for the 'View Flight Instructions' button.
    """

    # Initialize signals. Use for switching between views.
    sigStartTracking = qtc.pyqtSignal()
    sigReturnHome = qtc.pyqtSignal()
    def __init__(self, pilotName: str, instructorName: str, flightInstructions: str, flightData: str,
                 usingPreviousFlight: bool):
        """
        Class Constructor
        """
        qtw.QWidget.__init__(self)

        # Initiate the view
        self.initView(pilotName, instructorName, flightInstructions, flightData, usingPreviousFlight)

        # Format window
        self.setFixedSize(550, 550)

    def initView(self, pilotName: str, instructorName: str, flightInstructions: str, flightData: str,
                 usingPreviousFlight: bool):
        """
        Sets up the view and lays out all of the components.
        :param flightData: String containing path to flight data. Should be .flight file if usingPreviousFlight is
        true, or coordinates if usingPreviousFlight is false.
        :return: None
        """
        # Analyze the flight
        self.flightDict = {}

        if usingPreviousFlight is False:
            self.flightDict = self.analyzeFlight(flightData)
            self.flightDict["pilotName"] = pilotName
            self.flightDict["instructorName"] = instructorName
            self.flightDict["flightInstructions"] = flightInstructions
        else:
            self.flightDict = self.analyzeFlight(flightData)

        # Set up the title, flight information table, and statistics table.
        self.setWindowTitle('Report Screen')
        titleLayout = self.setupTitle()
        flInfoLayout = self.setupFlightInfo()
        statistics = self.createStatisticsTable()

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

        # Create a grid layout for all elements except the title.
        gridLayout = qtw.QGridLayout()
        gridLayout.addLayout(flInfoLayout, 0, 0)
        gridLayout.addWidget(statistics, 1, 0)
        gridLayout.addWidget(self.BtnViewGraphNoVelocity, 2, 0)
        gridLayout.addWidget(self.BtnViewGraphVelocity, 3, 0)
        gridLayout.addLayout(btnLayout, 4, 0)  # layout the buttons

        # Layout all of the above elements on a vertical layout
        vLayout = qtw.QVBoxLayout()
        vLayout.addLayout(titleLayout)
        vLayout.addLayout(gridLayout)

        # Attach the layout to the screen
        self.setLayout(vLayout)

    def signalExportResults(self):
        """
        Sends a signal to the main controller that the Export Results button was pushed.
        """
        # Save flight results to .flight file.
        outPath = '../Export/ExportedFiles/' + self.flightDict["pilotName"] + '.flight'
        Export.ExportFile.export_data(self.flightDict, outPath)

        # Show message box saying that exporting was completed.
        msgBox = qtw.QMessageBox()
        msgBox.setText(
            "Results exported!")
        msgBox.exec()

    def signalStartTracking(self):
        """
        Sends a signal to the main controller that the Fly Again button was pushed.
        :return: none
        """
        self.sigStartTracking.emit()

    def signalReturnHome(self):
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

    def setupGraph(self, flightData: dict, displayVelocity: bool):
        """
         Sets up the 3d plot for viewing upon click of button. displayVelocity is a boolean denoting if the graph should
         display colored segments for velocity.
         :param flightData: dictionary of flight data
         :param displayVelocity: Bool denoting if velocity should be plotted or not.
         :return: None
         """
        # Generate and show graph
        fig = Graph.generateGraph(flightData, displayVelocity)

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

    def showWindow(self):
        """
        Takes all of the elements from the view and displays the window.
        :return: None
        """
        self.window.show()

    def createStatisticsTable(self):
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

        self.tableWidget.setItem(0, 0, qtw.QTableWidgetItem("Smoothness"))
        self.tableWidget.setItem(0, 1, qtw.QTableWidgetItem(str(self.flightDict["smoothness"])))
        self.tableWidget.setItem(1, 0, qtw.QTableWidgetItem("Average Velocity Change"))
        self.tableWidget.setItem(1, 1, qtw.QTableWidgetItem(str(round(self.flightDict["avgVel"], 2)) + ' m/s'))
        self.tableWidget.setItem(2, 0, qtw.QTableWidgetItem("Minimum Velocity Change"))
        self.tableWidget.setItem(2, 1, qtw.QTableWidgetItem(str(round(self.flightDict["minVel"], 2)) + ' m/s'))
        self.tableWidget.setItem(3, 0, qtw.QTableWidgetItem("Maximum Velocity Change"))
        self.tableWidget.setItem(3, 1, qtw.QTableWidgetItem(str(round(self.flightDict["maxVel"], 2)) + ' m/s'))

        # Make non-editable
        self.tableWidget.setEditTriggers(qtw.QTableWidget.NoEditTriggers)

        return self.tableWidget

    def analyzeFlight(self, filePath: str):
        """
        Analyzes the flight data to extract coordinates, velocity values, and statistics.
        :param filePath: String representing file path where dictionary is stored.
        :return: Arrays of x and y and z coordinates, array of velocity values, average velocity, standard deviation,
        maximum velocity, minimum velocity.
        """
        # Read in dictionary
        flightDict = Graph.readCoordinates(filePath)

        # Update flight dict to contain velocity
        flightDict1 = Graph.velocityPoints(flightDict)

        # Update flight dict to contain statistics on velocity points
        flightDict2 = Graph.computeVelocityStatistics(flightDict1)

        return flightDict2

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
    def set_LblPilot(self, lbl: qtw.QLabel):
        """
        Setter for the pilot Label.
        :param lbl: The label we want to replace the current one with.
        :return: None
        """
        self.__lblPilot = lbl

    @LblPilot.deleter
    def del_LblPilot(self):
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
    def set_LblInstructor(self, lbl: qtw.QLabel):
        """
        Setter for the instructor Label.
        :param lbl: The label we want to replace the current one with.
        :return: None
        """
        self.__lblInstructor = lbl

    @LblInstructor.deleter
    def del_LblInstructor(self):
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
    def set_LblFlightDate(self, lbl: qtw.QLabel):
        """
        Setter for the Flight date label.
        :param lbl: The label we want to replace the current one with.
        :return: None
        """
        self.__lblFlDate = lbl

    @LblFlightDate.deleter
    def del_LblFlightDate(self):
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
    def set_LblFlightLength(self, lbl: qtw.QLabel):
        """
        Setter for the flight length label.
        :param lbl: The label we want to replace the current one with.
        :return: None
        """
        self.__lblFlLength = lbl

    @LblFlightLength.deleter
    def del_LblFlightLength(self):
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
    def set_LblFlightInstructions(self, lbl: qtw.QLabel):
        """
        Setter for the flight instructions label.
        :param lbl: The label we want to replace the current one with.
        :return: None
        """
        self.__lblFlLengthInstructions = lbl

    @LblFlightInstructions.deleter
    def del_LblFlightInstructions(self):
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
    def set_BtnExport(self, btn: qtw.QPushButton):
        """
        The setter for the export button.
        :param btn: A Qt QPushButton we want to replace the export button with.
        :return: None
        """
        self.__btnExport = btn

    @BtnExport.deleter
    def del_BtnExport(self):
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
    def set_BtnFlyAgain(self, btn: qtw.QPushButton):
        """
        Setter for the fly again button.
        :param btn: A Qt QPushButton.
        :return: None
        """
        self.__btnFlyAgain = btn

    @BtnFlyAgain.deleter
    def del_BtnFlyAgain(self):
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
    def set_BtnHome(self, btn: qtw.QPushButton):
        """
        Setter for the home button.
        :param btn: A Qt QPushButton.
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
    def BtnViewGraphVelocity(self) -> qtw.QPushButton:
        """
        The home for the view graph with velocity button.
        :return: None
        """
        return self.__btnViewGraphVelocity

    @BtnViewGraphVelocity.setter
    def set_BtnViewGraphVelocity(self, btn: qtw.QPushButton):
        """
        Setter for the view graph with velocity button.
        :param btn: A Qt QPushButton.
        :return: None
        """
        self.__btnViewGraphVelocity = btn

    @BtnViewGraphVelocity.deleter
    def del_BtnViewGraphVelocity(self):
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
    def set_BtnViewGraphNoVelocity(self, btn: qtw.QPushButton):
        """
        Setter for the view graph without velocity button.
        :param btn: A Qt QPushButton.
        :return: None
        """
        self.__btnViewGraphNoVelocity = btn

    @BtnViewGraphNoVelocity.deleter
    def del_BtnViewGraphNoVelocity(self):
        """
        Deleter for the view graph without velocity button. Never call this.
        :return: None
        """
        del self.__btnViewGraphNoVelocity

    # endregion