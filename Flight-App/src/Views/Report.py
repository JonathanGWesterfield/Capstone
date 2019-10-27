#!/usr/bin/env python
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import src.Views.Graph as Graph
import matplotlib.pyplot as plt
import datetime as dt
from src.Views.BaseUI import BaseView
import PyQt5.QtGui as qtg

class ReportView(BaseView):

    def __init__(self):
        super().__init__()
        self.initView()

    def initView(self):
        """
        Creates the view with all of the control and display elements.
        :return: None
        """
        titleLayout = self.setupTitle()
        flInfoLayout = self.setupFlightInfo()
        statistics = self.createTable()

        gridLayout = qtw.QGridLayout()
        gridLayout.addLayout(flInfoLayout, 0, 0)
        gridLayout.addWidget(statistics, 1, 0)
        btn = qtw.QPushButton('View Flight Path')
        btn.clicked.connect(self.setupGraph)
        gridLayout.addWidget(btn, 2, 0)
        gridLayout.addLayout(self.setButtonLayout(), 3, 0) # layout the buttons

        vLayout = qtw.QVBoxLayout()
        vLayout.addLayout(titleLayout)
        vLayout.addLayout(gridLayout)

        # Attach the layout to the screen
        self.window = qtw.QWidget()
        self.window.setLayout(vLayout)

    def setupTitle(self) -> qtw.QVBoxLayout:
        """
        Sets up the title with the application title on top and the name of the screen just below it.
        :return: Layout with the application title and screen title labels
        """
        lblTitle = qtw.QLabel(self.get_appName())
        lblTitle.setFont(self.TitleFont)
        lblTitle.setAlignment(qtc.Qt.AlignCenter)

        lblScreenTitle = qtw.QLabel('Flight Report')
        lblScreenTitle.setFont(self.MediumFont)
        lblScreenTitle.setAlignment(qtc.Qt.AlignCenter)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(lblTitle)
        vbox.addWidget(lblScreenTitle)

        return vbox

    def setupFlightInfo(self) -> qtw.QGridLayout:
        """
        Sets up the flight info (pilot, instructor, date, length, and smoothness score) in a grid so it gets laid out nice and pretty.
        :return: Grid layout of the flight information
        """
        # Setup all labels with default values for testing and detecting errors in the controls
        self.__lblPilot = qtw.QLabel('None')
        self.__lblInstructor = qtw.QLabel('None')
        self.__lblFlDate = qtw.QLabel(dt.date.today().strftime('%m/%d/%Y'))
        self.__lblFlLength = qtw.QLabel('00:00:00')
        self.__lblFlSmoothness = qtw.QLabel('0')

        grid = qtw.QGridLayout()
        flightInfoTitle = qtw.QLabel('Flight Information')
        flightInfoTitle.setFont(qtg.QFont("Helvetica Neue", 16, qtg.QFont.Bold))
        grid.addWidget(flightInfoTitle, 0, 0)
        grid.addWidget(qtw.QLabel('Pilot: '), 1, 0)
        grid.addWidget(self.__lblPilot, 1, 1)
        grid.addWidget(qtw.QLabel('Instructor: '), 2, 0)
        grid.addWidget(self.__lblInstructor, 2, 1)
        grid.addWidget(qtw.QLabel('Flight Date: '), 3, 0)
        grid.addWidget(self.__lblFlDate, 3, 1)
        grid.addWidget(qtw.QLabel('Flight Length: '), 4, 0)
        grid.addWidget(self.__lblFlLength, 4, 1)

        statisticsInfoTitle = qtw.QLabel('Statistics')
        statisticsInfoTitle.setFont(qtg.QFont("Helvetica Neue", 16, qtg.QFont.Bold))
        grid.addWidget(statisticsInfoTitle, 5, 0)

        return grid

    def setupGraph(self):
        """
         Sets up the 3d plot for viewing upon click of button.
         :return: None
         """
        # fig = plt.figure()
        # Import coordinates
        x, y, z = Graph.readCoordinates('../Tests/TestFiles/coordinates_tiny.rtf')
        # Generate and show graph
        fig = Graph.genGraph(x, y, z)

        # Define manager so figure can be viewed upon button click
        new_manager = fig.canvas.manager
        new_manager.canvas.figure = fig
        fig.set_canvas(new_manager.canvas)
        fig.show()

    def setButtonLayout(self) -> qtw.QHBoxLayout:
        """
        Lays out the 'Export Results', 'Fly Again' and 'Import Previous Flight' buttons into a horizontal layout to be
        put on screen.
        :return: The horizontal layout containing the 3 buttons
        """
        self.__btnTestConfig = qtw.QPushButton('Export Results')
        self.__btnStart = qtw.QPushButton('Fly Again')
        self.__btnImport = qtw.QPushButton('Return to Home')

        buttonBox = qtw.QHBoxLayout()
        buttonBox.addWidget(self.__btnTestConfig)
        buttonBox.addWidget(self.__btnStart)
        buttonBox.addWidget(self.__btnImport)

        return buttonBox

    def showWindow(self):
        """
        Takes all of the elements from the view and displays the window.
        :return: None
        """
        self.window.show()
        # self.app.exec_()

    def createTable(self):
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
        self.tableWidget.setItem(0, 1, qtw.QTableWidgetItem("Smoothness Value"))
        self.tableWidget.setItem(1, 0, qtw.QTableWidgetItem("Average Velocity"))
        self.tableWidget.setItem(1, 1, qtw.QTableWidgetItem("Average Velocity Value"))
        self.tableWidget.setItem(2, 0, qtw.QTableWidgetItem("Minimum Velocity"))
        self.tableWidget.setItem(2, 1, qtw.QTableWidgetItem("Minimum Velocity Value"))
        self.tableWidget.setItem(3, 0, qtw.QTableWidgetItem("Maximum Velocity"))
        self.tableWidget.setItem(3, 1, qtw.QTableWidgetItem("Maximum Velocity Value"))

        return self.tableWidget

    #region > Report View Properties

    #region > Pilot Label Property
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
    #endregion

    #region > Instructor Label Property
    @property
    def LblInstructor(self) -> qtw.QLabel:
        """
        Getter for the instructor label so we can attach functionality to it in the child class.
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
    #endregion

    #region > Flight Date Property
    @property
    def LblFlightDate(self) -> qtw.QLabel:
        """
        Getter for the flight date label so we can attach functionality to it in the child class.
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
    #endregion

    #region > Flight Length Label Property
    @property
    def LblFlightLength(self) -> qtw.QLabel:
        """
        Getter for the flight length label so we can attach functionality to it in the child class.
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
    #endregion

    #region > 3D Matplot Plot Property
    @property
    def PltFlightPlot(self):
        """
        Getter for the flight plot so we can populate it with data and format it further in the child class.
        :return: Reference to the 3D flight plot.
        """
        return self.__line

    @PltFlightPlot.setter
    def set_PltFlightPlot(self, fig: plt.Figure):
        """
        Setter for the 3D flight plot.
        :param fig: The figure we want to replace the current one with (I might have the wrong type indicated)
        :return: None
        """
        self.__line = fig

    @PltFlightPlot.deleter
    def del_PltFlightPlot(self):
        """
        Deleter for the 3D flight plot.
        :return: None
        """
        del self.__line
    #endregion

    #endregion


app = qtw.QApplication([])

ui = ReportView()
ui.showWindow()

app.exec()

