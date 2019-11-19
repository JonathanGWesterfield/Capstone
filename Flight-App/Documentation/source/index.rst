.. Drone Tracker documentation master file, created by
   sphinx-quickstart on Mon Nov 18 16:37:18 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Drone Tracker's documentation!
=========================================

Intro
~~~~~~~~~~~~~

Version 1.0.3

Written by: Hayley Eckert, Jonathan Westerfield, Donald Elrod, and Ismael Rodriguez

This application is the controller for the entire project. It interfaces with the cell phones and controls them in order to record footage of a drone flight. It will then open 2 OpenCV processes in order to analyze the footage from the cell phones. 

This flight application relies on `OpenCV <https://opencv.org/>`_ and `MatPlotLib <https://matplotlib.org/>`_.


The main sections of the application are as follows:
 * Program_Controller:
    Starts up the entire Drone Tracker program the user interacts with
 * PhoneController:
    Sends and receives network signals from the phone over TCP to control the phone.
 * OpenCV:
    Takes the file of the video transferred from the phone and extracts the coordinates of the drone from the footage

.. toctree::
   :maxdepth: 3
   :caption: Contents:



Program Controller
==================
.. automodule:: src.Controllers.Program_Controller
    :members:

OpenCV
===================
.. automodule:: src.Controllers.OpenCVThreadedController
    :members:

Exceptions
=======================
.. automodule:: src.Controllers.Exceptions
    :members:

PhoneController
============================
.. automodule:: src.Controllers.PhoneController
    :members:

Export Flight
==========================
.. automodule:: src.Export.ExportFile
    :members:

Import Flight
==========================
.. automodule:: src.Export.ImportFile
    :members:

Loading Screen
===========================
.. automodule:: src.Views.View_LoadingScreen
    :members:

Report Screen
==========================
.. automodule:: src.Views.View_ReportScreen
    :members:

Startup Screen
===========================
.. automodule:: src.Views.View_StartupScreen
    :members:

Tracking Screen
============================
.. automodule:: src.Views.View_TrackingScreen
    :members:

Verify Setup Screen
================================
.. automodule:: src.Views.View_VerifySetupScreen
    :members:

MatPlot Graph
==========================
.. automodule:: src.Views.Graph
    :members:

Graph Test
==========
.. automodule:: src.Tests.Graph_Test
    :members:

Import File Test
================
.. automodule:: src.Tests.ImportFile_Test
    :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
