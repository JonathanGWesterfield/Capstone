#!/usr/bin/env python
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
        FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

import datetime as dt

from src.Views.BaseUI import BaseView

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
        graph = self.setupPlot()
        flInfoLayout = self.setupFlightInfo()

        gridLayout = qtw.QGridLayout()
        gridLayout.addLayout(flInfoLayout, 0, 0)
        gridLayout.addWidget(graph, 1, 0)

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
        grid.addWidget(qtw.QLabel('Pilot: '), 0, 0)
        grid.addWidget(self.__lblPilot, 0, 1)
        grid.addWidget(qtw.QLabel('Instructor: '), 1, 0)
        grid.addWidget(self.__lblInstructor, 1, 1)
        grid.addWidget(qtw.QLabel('Flight Date: '), 2, 0)
        grid.addWidget(self.__lblFlDate, 2, 1)
        grid.addWidget(qtw.QLabel('Flight Length: '), 3, 0)
        grid.addWidget(self.__lblFlLength, 3, 1)
        grid.addWidget(qtw.QLabel('Flight Smoothness Score: '), 4, 0)
        grid.addWidget(self.__lblFlSmoothness, 4, 1)

        return grid

    def setupPlot(self):
        """
        Uses a line plot and a scatter plot on the same graph so we can have points connected by lines
        on the graph. Found how to do it here:
        https://stackoverflow.com/questions/44355546/how-to-connect-points-in-python-ax-scatter-3d-plot
        :return: A 3D plot that we can put information into later
        :todo: IMPROVE THIS MAKE IT INTERACTIVE AGAIN (DRAGGING)
        """
        vbox = qtw.QVBoxLayout()
        x, y, z = [1, 1.5, 3, 5], [1, 2.4, 3, 7], [3.4, 1.4, 1, 10]

        fig = plt.figure()

        self.__line = fig.add_subplot(1, 1, 1, projection='3d')
        self.__line.plot(x, y, z, color='r')
        self.__line.scatter(x, y, z, c='r')

        canvas = FigureCanvas(fig)
        vbox.addWidget(canvas)

        return canvas

    def setButtonLayout(self) -> qtw.QHBoxLayout:
        """
        Lays out the 'Test Config', 'Start' and 'Import' buttons into a horizontal layout to be
        put on screen.
        :return: The horizontal layout containing the 3 buttons
        """
        self.__btnTestConfig = qtw.QPushButton('Verify Camera Setup')
        self.__btnStart = qtw.QPushButton('Start Tracking')
        self.__btnImport = qtw.QPushButton('Import Previous Flight')

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

