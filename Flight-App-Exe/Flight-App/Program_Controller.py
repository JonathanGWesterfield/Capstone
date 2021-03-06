#!/usr/bin/env python3

import sys
import os
import signal
import subprocess
import shutil
import glob
import time 
import re
import json
from multiprocessing import Process
from PyQt5 import QtWidgets as qtw, QtCore as qtc
from View_TrackingScreen import TrackingWindow
from View_StartupScreen import StartupWindow
from View_VerifySetupScreen import VerifySetupWindow
from View_ReportScreen import ReportWindow
from View_LoadingScreen import LoadingWindow
from PhoneController import PhoneControl as PhoneControl
# from Controllers.RPIController import RPIController as RPIController
from OpenCVThreadedController import merge_data_points, DroneTracker
from ImportFile import importData

class Controller:
    """
    Controller class for the application. Changes between application views based on user input.
    Run this file in order to begin the application.
    """

    def __init__(self, phoneControl: PhoneControl) -> None:
        """
        Class constructor. Creates an empty .flight file structure to be overwritten by the flight
        output from the opencv processes.

        :param phoneControl: The phone controller object used to send/receive signals to/from the phones.
        """
        self.pilotName = ''
        self.instructorName = ''
        self.flightInstructions = ''
        self.flightModeEnabled = False
        self.phoneControl = phoneControl
        # self.rpiControl = rpiControl
        self.flightDict = {
            "pilotName": "",
            "instructorName": "",
            "flightInstr": "",
            "flightDate": "",
            "flightLength": 0.0,
            "coords": [],
            "velocities": [],
            "avgVel": 0.0,
            "maxVel": 0.0,
            "minVel": 0.0,
            "smoothness": 0.0,
            "legalPoints": []
        }

        self.setupFileStructure() # setup the file structure needed for the program
        self.cleanup() # make sure we start with a clean file directory structure (except for past .flight files)

    def show_home(self) -> None:
        """
        Loads the home startup screen for the user.

        :return: None
        """
        # Close previous window.
        try:
            self.tracking_window.close()
        except:
            print("Tracking window not open")
        try:
            self.window.close()
        except:
            print("Main window not open")
        try:
            self.verify_screen.close()
        except:
            print("Verify screen window not open")
        try:
            self.report_window.close()
        except:
            print("Report window not open")
        try:
            self.loading_window.close()
        except:
            print("Loading window not open")

        # Initialize home startup screen by instantiating StartupWindow class.
        self.home = StartupWindow(self.flightModeEnabled)

        # Attach functionality to signals in StartupWindow.
        # Signals are generated by the StartupWindow class when a button is pushed to change views.
        self.home.sigVerifySetup.connect(self.show_verify_screen)
        self.home.sigStartTracking.connect(self.show_tracking_window)

        # Import previous flight
        self.home.sigImportFlight.connect(self.import_flight)

        # Show the screen
        self.home.show()

    def import_flight(self, flightPath: str) -> None:
        """
        Reads in a .flight file and displays the report view for it.

        :param flightPath: String with file path of chosen file to import.
        :return: None
        """
        if flightPath != '':
            print('Importing file ' + flightPath)
            self.show_report_window(flightPath, True, {})

    def show_verify_screen(self) -> None:
        """
        Loads the verify setup screen for the user.

        :return: None
        """
        # Initialize verify setup screen by instantiating VerifySetupWindow class.
        self.verify_screen = VerifySetupWindow(self.phoneControl) #, self.rpiControl)

        # Attach functionality to signals in VerifySetupWindow.
        # Signals are generated by the VerifySetupWindow class when a button is pushed to change views.
        self.verify_screen.sigReturnHome.connect(self.show_home)
        self.verify_screen.sigGoodToFly.connect(self.updateFlightStatus)

        # Close previous screen.
        try:
            self.home.close()
        except:
            print("Home window not open")

        # Show verify setup screen.
        self.verify_screen.show()

    def updateFlightStatus(self) -> None:
        """
        Sets the status of the system verification test.

        :return: none
        """
        self.flightModeEnabled = True

    def show_tracking_window(self) -> None:
        """
        Loads the tracking screen for the user.

        :return: None
        """
        # Close report window if open.
        try:
            self.report_window.close()
        except:
            print("Report window not open")

        # Initialize the tracking screen by instantiating TrackingWindow class.
        self.tracking_window = TrackingWindow(self.phoneControl)

        # Attach functionality to signals in TrackingWindow.
        # Signals are generated by the TrackingWindow class when a button is pushed to change views.
        self.tracking_window.sigReturnHome.connect(self.show_home)
        self.tracking_window.sigStopTracking.connect(self.show_loading_window)
        self.tracking_window.sigFlightInfoConfirmed.connect(self.get_flight_info)

        # Close the previous screen.
        try:
            self.home.close()
        except:
            print("Home window not open")

        # Show the tracking screen.
        self.tracking_window.show()

    def get_flight_info(self, pilotName: str, instructorName: str, flightInstructions: str) -> None:
        """
         Saves the pilot name, instructor name, and flight instructions once confirmed by the user.

         :param pilotName: String containing the pilot name
         :param instructorName: String containing the instructor name
         :param flightInstructions: String containing the flight instructions
         :return: None
         """
        self.pilotName = pilotName
        self.instructorName = instructorName
        self.flightInstructions = flightInstructions

    def show_report_window(self, previousFlight: str, usingPreviousFlight: bool, flightData: dict) -> None:
        """
        Loads the report screen for the user.

        :param previousFlight: String containing path to flight data. Should be .flight file if usingPreviousFlight is true, or empty if usingPreviousFlight is false.
        :param usingPreviousFlight: Boolean representing if the report view is for an existing .flight file or a new analysis.
        :param flightData: Dictionary containing the flight data. Should be populated with only coordinates if usingPreviousFlight is false, and empty if usingPreviousFlight is true.
        :return: None
        """
        # Initialize the report by instantiating ReportWindow class.
        self.report_window = ReportWindow(self.pilotName, self.instructorName, self.flightInstructions,
                                          previousFlight, usingPreviousFlight, flightData)

        # Attach functionality to signals in ReportWindow.
        # Signals are generated by the ReportWindow class when a button is pushed to change views.
        self.report_window.sigReturnHome.connect(self.show_home)
        self.report_window.sigStartTracking.connect(self.show_tracking_window)

        # Close the previous screen.
        try:
            if usingPreviousFlight is False:
                self.loading_window.close()
            else:
                self.home.close()
        except:
            print("Error")

        # Show the report screen.
        self.report_window.show()

    def show_loading_window(self) -> None:
        """
        Loads the loading screen for the user.

        :return: None
        """
        # Initialize the report by instantiating LoadingWindow class.
        self.loading_window = LoadingWindow()

        # Attach functionality to signals in LoadingWindow.
        # Signals are generated by the LoadingWindow class when a button is pushed to change views.
        self.loading_window.sigReturnHome.connect(self.show_home)

        self.cleanup() # make sure we sterilize our destination directories

        # Show report view on flight coordinates.
        self.loading_window.sigTestReport.connect(lambda *args: self.show_report_window("", False, flightData))
        self.loading_window.sigTransferFootage.connect(lambda *args: self.transfer_footage(self.phoneControl))

        # Close the previous screen.
        try:
            self.tracking_window.close()
        except:
            print("Error")

        # Show the loading screen.
        self.loading_window.show()

        print("Window shown")

    def setupFileStructure(self) -> None:
        """
        Sets up the folders that need to exist before we can transfer footage and analyze. The file structure
        should be: drone-tracker > FTP, opencv-output, Flights. This makes it easier to keep track of
        the files that we are working with during the application lifecycle.

        :return: None
        """
        self.pathToFiles = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/drone-tracker/')
        self.pathToFTPDir = self.pathToFiles + 'FTP/'
        self.pathToOpenCVDir = self.pathToFiles + 'opencv-output/'
        self.pathToFlightsDir = self.pathToFiles + 'Flights/'


        # make sure that ~/Desktop/drone-tracker directory exists
        if not os.path.exists(self.pathToFiles):
            os.mkdir(self.pathToFiles)

        # make sure that the ~/Desktop/drone-tracker/FTP directory exists for transferring footage from
        # the phone to the laptop.
        if not os.path.exists(self.pathToFTPDir):
            os.mkdir(self.pathToFTPDir)

        # make sure that the ~/Desktop/drone-tracker/opencv-output directory exists for the image processing
        if not os.path.exists(self.pathToOpenCVDir):
            os.mkdir(self.pathToOpenCVDir)

        # make sure that the ~/Desktop/drone-tracker/Flights directory exists for depositing completed flight files
        # after a flight has been analyzed
        if not os.path.exists(self.pathToFlightsDir):
            os.mkdir(self.pathToFlightsDir)

        return

    def cleanup(self) -> None:
        """
        Goes through our file structure and deletes all files (except anything in the Flight folder).
        This is for when we are done with the program and want to delete the raw footage from the phone,
        the output points from the opencv processing and any other files that were used during the
        program execution. Should also be called before any time the user wants to fly.

        :return: None
        """
        # Delete everything in the FTP folder
        for the_file in os.listdir(self.pathToFTPDir):
            file_path = os.path.join(self.pathToFTPDir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path) # Delete all subfolders
            except Exception as e:
                print(e)

        # Delete everything in the opencv-output folder
        for the_file in os.listdir(self.pathToOpenCVDir):
            file_path = os.path.join(self.pathToOpenCVDir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path) # Delete all subfolders
            except Exception as e:
                print(e)

        return

    def get_all_files(self, folderPath:str) -> list:
        """
        Will get all of the file names in a folder. This will be used after the video footage is transferred from
        the phone to the laptop. We need to grab the 2 videos filenames in the folder in order to send them to
        the opencv analysis to have the coordinates extracted. This will also be used when we need to splice
        together all of the coordinates output by the OpenCVController json files.

        :param folderPath: The directory that we need to get all of the files from.
        :return: A list of all of the file names in that directory
        """
        files = []

        with os.scandir(folderPath) as entries:
            for entry in entries:
                if entry.is_file():
                    files.append(entry.name)

        return files

    def get_in_order(self, files:list) -> list:
        """
        Will return the file names in order. This means that phone-1 will be first in the list and
        phone-2 will be second. Need this to ensure that a specific phone's coordinates are being
        used for the Z, X axis and the other is used for Z, Y

        :param files: The list of files we get from the get_all_files() function
        :return: The list of file names starting with phone-1 first and phone-2 second
        """
        # should only have 2 files in the folder

        print("Num Files in directory: ", len(files))
        if not(len(files) == 2):
            raise Exception("More files in the directory than was expected!!")



        inOrder = []

        # this is very dirty but I'm in a hurry
        file1 = str(files[0])
        file2 = str(files[1])

        file1Tokens = re.split('_|\.', file1)
        file2Tokens = re.split('_|\.', file2)

        if (file1Tokens[-2] == 'phone-1'):
            inOrder.append(file1)
            inOrder.append(file2)
            return inOrder

        inOrder.append(file2)
        inOrder.append(file1)

        return inOrder


    def transfer_footage(self, phoneControl: PhoneControl) -> None:
        """
        Transfers footage and calls DroneController to analyze the footage.

        :param phoneControl: Phone Controller object for the active phone connection.
        :return: none
        """

        try:
            # Call the functions to transfer the files
            phoneControl.startFileTransfer(self.pathToFTPDir)
            phoneControl.waitForFileTransfer()

            self.start_analysis()

        except Exception as e:
            msgBox = qtw.QMessageBox()
            msgBox.setText(str(e))
            msgBox.exec()

    def start_analysis(self) -> None:
        """
        Spawns the sub processes that will analyze the footage of the drone footage. We will need
        to have the files before hand so we can pass them into each OpenCVController process.

        :return: None
        """
        # Get the files deposited into the FTP directory from the phone
        files = self.get_all_files(self.pathToFTPDir)
        files = self.get_in_order(files) # order the files

        file1 = self.pathToFTPDir + files[0]
        file2 = self.pathToFTPDir + files[1]

        print("Files to analyze: ", file1, ", ", file2)

        subprocess.Popen(['python3', 'OpenCVThreadedController.py', file1])
        subprocess.Popen(['python3', 'OpenCVThreadedController.py', file2])

        self.wait_for_analysis() # wait for the analysis of the files to complete

        return

    def wait_for_analysis(self) -> None:
        """
        Waits for the analysis of the footage to complete. Essentially is just a loop that checks to
        see if the file locks (*.lock) for our files are still in that directory. If they are, we wait,
        otherwise, we will exit the loop. From there, we need to get the output from those processes and splice
        the points together into a single 3D coordinate list.

        :return: None
        """
        finished = False

        time.sleep(3) # need to sleep to give some time for the opencv processes to start and create their .lock files
        while(not finished):
            lockFiles = glob.glob(self.pathToOpenCVDir + '*.lock') # find all files with a .lock extension
            if len(lockFiles) == 0:
                finished = True
            time.sleep(1) # sleep so we don't poll too frequently

        # get the output json so we can load up the data and splice together.
        files = self.get_all_files(self.pathToOpenCVDir)
        files = self.get_in_order(files)

        phone1Data = json.load(open(self.pathToOpenCVDir + files[0], 'r'))
        phone2Data = json.load(open(self.pathToOpenCVDir + files[1], 'r'))

        self.flightDict["coords"] = merge_data_points(phone1Data, phone2Data)
        self.flightDict["flightLength"] = self.flightDict["coords"][-1][0]

        print("Flight Length: ", self.flightDict["flightLength"])
        print(self.flightDict['coords'])

        self.transfer_complete(self.flightDict)


    def transfer_complete(self, flightData: dict) -> None:
        """
        Calls the report view using the flight data dictionary.

        :param flightData: Dictionary of flight data
        :return: none.
        """
        self.show_report_window("", False, flightData)

def createPhoneConnection(portNo) -> PhoneControl:
    """
    Creates a PhoneControl object used to commmunicate with the phones.

    :param portNo: Port number we are going to be listening for signals from the phone over.
    :return: PhoneControl object.
    """
    phoneControl = PhoneControl(portNo)
    return phoneControl

def close_conn(phoneControl: PhoneControl) -> None:
    """
    Closes the connection from the laptop to the phones.

    :param phoneControl: PhoneControl object containing the active connection.
    :return: None.
    """
    try:
        print("Connection closed")
        phoneControl.closeConn()
    except Exception as e:
        print(str(e))

def main() -> None:
    """
    Begins the main application.

    :return: None
    """
    # Create the main application.
    app = qtw.QApplication(sys.argv)

    # Create phone controller
    phoneControl = createPhoneConnection(8000)

    # Create the RPI controller
    # control = RPIController('localhost', '9876')
    # control = RPIController('192.168.1.2', '9876')

    # Create a controller for the application.
    controller = Controller(phoneControl=phoneControl) #, rpiControl=control)

    # Start the application on the home startup screen.
    controller.show_home()
    app.aboutToQuit.connect(lambda *args: close_conn(phoneControl))
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
