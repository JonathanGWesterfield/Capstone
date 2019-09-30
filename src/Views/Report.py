#!/usr/bin/env python
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
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
        :todo: IMPROVE THIS
        """
        vbox = qtw.QVBoxLayout()
        x, y, z = [1, 1.5, 3], [1, 2.4, 3], [3.4, 1.4, 1]

        fig = plt.figure()

        self.line = fig.add_subplot(1, 1, 1, projection='3d')
        self.line.plot(x, y, z, color='r')
        self.line.scatter(x, y, z, c='r')

        canvas = FigureCanvas(fig)
        vbox.addWidget(canvas)

        return canvas


    # from mpl_toolkits.mplot3d import Axes3D
    # import matplotlib.pyplot as plt
    # import numpy as np
    #
    # def randrange(n, vmin, vmax):
    #     '''
    #     Helper function to make an array of random numbers having shape (n, )
    #     with each number distributed Uniform(vmin, vmax).
    #     '''
    #     return (vmax - vmin) * np.random.rand(n) + vmin
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    #
    # n = 100
    #
    # # For each set of style and range settings, plot n random points in the box
    # # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
    # for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    #     xs = randrange(n, 23, 32)
    #     ys = randrange(n, 0, 100)
    #     zs = randrange(n, zlow, zhigh)
    #     ax.scatter(xs, ys, zs, c=c, marker=m)
    #
    # ax.set_xlabel('X Label')
    # ax.set_ylabel('Y Label')
    # ax.set_zlabel('Z Label')
    #
    # plt.show()

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

