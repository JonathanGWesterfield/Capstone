#!/usr/bin/env python
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.figure import Figure

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
        # gridLayout.addWidget(graph, 0, 0)


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
        Sets up the flight info (pilot, instructor, date) in a grid so it gets laid out nice and pretty.
        :return: Grid layout of the flight information
        """
        # Setup all labels with default values for testing and detecting errors in the controls
        self.__lblPilot = qtw.QLabel('None')
        self.__lblInstructor = qtw.QLabel('None')
        self.__lblFlDate = qtw.QLabel(dt.date.today().strftime('%m/%d/%Y'))
        self.__lblFlLength = qtw.QLabel('00:00:00')

        grid = qtw.QGridLayout()
        grid.addWidget(qtw.QLabel('Pilot: '), 0, 0)
        grid.addWidget(self.__lblPilot, 0, 1)
        grid.addWidget(qtw.QLabel('Instructor: '), 1, 0)
        grid.addWidget(self.__lblInstructor, 1, 1)
        grid.addWidget(qtw.QLabel('Flight Date: '), 2, 0)
        grid.addWidget(self.__lblFlDate, 2, 1)
        grid.addWidget(qtw.QLabel('Flight Length: '), 3, 0)
        grid.addWidget(self.__lblFlLength, 3, 1)

        return grid

    def setupPlot(self):
        """
        Uses a line plot and a scatter plot on the same graph so we can have points connected by lines
        on the graph. Found how to do it here:
        https://stackoverflow.com/questions/44355546/how-to-connect-points-in-python-ax-scatter-3d-plot
        :return: A 3D plot that we can put information into later
        """
        canvas = FigureCanvas(Figure(figsize=(5, 3)))

        self.__graph = plt.plot(projection="3d")

        return self.__graph


    def showWindow(self):
        """
        Takes all of the elements from the view and displays the window.
        :return: None
        """
        self.window.show()
        # self.app.exec_()



app = qtw.QApplication([])

ui = ReportView()
ui.showWindow()

app.exec()

