import socket
import datetime
from Signal import Signals
import sys
import os
from Exceptions import RecordingNotStartedException, TransferNotStartedException, PhonesNotSyncedException

# import thread module
from _thread import *
import threading

class PhoneControl:
    """
    This class is for communicating with and controlling the phones out in the field. It uses simple
    TCP connections with each phone in order to control them.
    """

    def __init__(self, portNum: int):
        """
        Initializes the server
        :param portNum: The port that we are going to be listening for connections on.
        """
        self.portNum = portNum
        self.host = ""
        self.maxClients = 2 # We will have 2 phones therefore 2 network connections on this port
        self.connections = [] # list of our connections
        self.connected = False
        self.transferring = False
        self.recording = False

        self.socket = self.setupSocket()

    def synced(self) -> bool:
        """
        The getter function for seeing if the phones synced or not.
        :return: True if they have been synced, false otherwise
        """
        return self.connected

    def isTransferring(self) -> bool:
        """
        A flag for us to access to see if the system is still waiting for the video to finish the file
        transfer of the videos it recorded.
        :return: True if the video has finished transferring, false otherwise.
        """
        return self.transferring

    def setupSocket(self):
        """
        Creates the socket that we will use to listen for incoming connections
        :return: None
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.portNum))

        print("Socket binded to port: ", self.portNum)

        sock.listen(5)
        print("Socket is listening for connections")

        return sock

    def closeConn(self):
        """
        Closes all of the connections and the socket.
        :return: None
        """
        # Make sure the phones are connected and synced first
        if not self.connected:
            raise PhonesNotSyncedException("ERROR: Phones not synced up yet!")

        for conn in self.connections:
            conn.close()

        self.socket.close()

        self.connected = False

    def sync(self):
        """
        This function will wait until both phones have been connected to this app.
        :return: None
        """
        while(len(self.connections) < self.maxClients):
            conn, addr = self.socket.accept()

            # increment the number of connections we have
            if not (conn is None):
                self.connections.append(conn) # add the connection to our list for later actions
                print("Phone Connection: ", str(conn))

        self.connected = True

    def threadSendSignal(self,conn: socket.socket, signal: str, sigMessage: str, sigAck: str):
        """
        This function takes a signal and the expected output so that we don't have to rewrite the same code for
        every action we have with the phones.
        :param conn: A socket connection to a phone that has already been opened.
        :param signal: The Signal we want to send to the phone. Valid options are: START, STOP, and START_FTP
        :param sigMessage: A message that we want to send alongside the signal for the phone to use.
        :param sigAck: The Signal we expect to get back from the phone in response to our signal. Valid options
            are: START_ACKNOWLEDGE, STOP_ACKNOWLEDGE, START_FTP_ACKNOWLEDGE
        :return: None
        """
        try:
            # Send the stop command to the phone
            timestamp = datetime.datetime.now()
            command = bytes((signal + ";" + sigMessage + "\n"), 'utf-8') # need the '\n' char or the connection will hang

            print("Sending the " + signal + " Signal")
            conn.sendall(command)
            print(signal + " signal sent.\nWaiting for acknowledgment\n")

            # Wait for the start acknowledgement
            message = conn.recv(1024)

            if message is None:
                raise Exception('ERROR! Phone should have said something by now!\n')

            message = message.decode('utf-8').strip()

            # If the function fails here it was going to be wrong anyway
            if message == sigAck:
                print("Success! The phone acknowledged the " + signal + " command\n")
                return

            if message == "ILLEGAL":
                raise Exception("ERROR! Phone sent back an illegal response!\n")

            errorMsg = "ERROR! Response received is not anything we expected! Recieved: " + message + "\n"
            raise Exception(errorMsg)

        except Exception as e:
            self.closeConn()
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def startRecording(self):
        """
        Call this in order to send a signal to the phones that they need to start recording.
        :return:
        """
        threads = list()

        # Make sure the phones are connected and synced first
        if not self.connected:
            raise PhonesNotSyncedException("ERROR: Phones not synced up yet!")

        try:
            for conn in self.connections:
                # Start a new thread and return its identifier
                timestamp = datetime.datetime.now()
                x = threading.Thread(target=self.threadSendSignal, args=(conn, "START", str(timestamp), "START_ACKNOWLEDGE"))
                threads.append(x)
                x.start()

            for index, thread in enumerate(threads):
                thread.join()
            self.recording = True
            print("Start Threads Joined!\n")

        except Exception as e:
            self.closeConn()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def stopRecording(self):
        """
        Call this in order to send a signal to the phones that they need to stop tracking. Sends both
        phones a stop signal and the name of the file path that they will need to send their
        videos to over FTP.
        :return: None
        """
        # Make sure the phones are connected and synced first
        if not self.connected:
            raise PhonesNotSyncedException("ERROR: Phones not synced up yet!")

        # make sure that we are recording first
        if not self.recording:
            raise RecordingNotStartedException("ERROR! Recording must be started to be stopped")

        threads = list()

        try:
            for conn in self.connections:
                # Start a new thread and return its identifier
                timestamp = datetime.datetime.now()
                x = threading.Thread(target=self.threadSendSignal, args=(conn, "STOP", str(timestamp), "STOP_ACKNOWLEDGE"))
                threads.append(x)
                x.start()

            for index, thread in enumerate(threads):
                thread.join()

            self.recording = False
            print("Stop Threads Joined!\n")

        except Exception as e:
            self.closeConn()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def startFileTransfer(self, filepath: str):
        """
        Will send a signal to the phone that tells it to transfer the video files it recorded over to the laptop
        by opening an FTP connection.
        :param filepath: The file path on our laptop that the phones will need to send their videos to over FTP.
        :return: None
        """
        # Make sure the phones are connected and synced first
        if not self.connected:
            raise PhonesNotSyncedException("ERROR: Phones not synced up yet!")

        threads = list()

        try:
            for conn in self.connections:
                # Start a new thread and return its identifier
                x = threading.Thread(target=self.threadSendSignal, args=(conn, "START_FTP", filepath, "START_FTP_ACKNOWLEDGE"))
                threads.append(x)
                x.start()

            for index, thread in enumerate(threads):
                thread.join()

            print("Start FTP Threads Joined!\n")
            self.transferring = True # Set flag that we are currently transferring the file over

        except Exception as e:
            self.closeConn()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def waitForFileTransfer(self):
        """
        Spawns threads that will wait for both phones to send a signal saying that the file transfer
        of the videos is complete.
        :return: None
        """
        # Make sure the phones are connected and synced first
        if not self.connected:
            raise PhonesNotSyncedException("ERROR: Phones not synced up yet!")

        threads = list()

        if not self.transferring:
            raise TransferNotStartedException("ERROR! Transfer has not been started! Can't wait for it!")

        try:
            for conn in self.connections:
                # Start a new thread and return its identifier
                x = threading.Thread(target=self.threadWaitForFileTransfer, args=(conn,))
                threads.append(x)
                x.start()

            for index, thread in enumerate(threads):
                thread.join()

            print("Start FTP Threads Joined!\n")
            self.transferring = False  # Set flag that we are currently transferring the file over

        except Exception as e:
            self.closeConn()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def threadWaitForFileTransfer(self, conn: socket.socket):
        """
        This is a thread for waiting for the signal from the phone that the file transfer to the filepath specified
        in the startFileTransfer() function arguments.
        :param conn: A socket connection to a phone that has already been opened.
        :return: None
        """
        try:
            # Wait for the start acknowledgement
            message = conn.recv(1024)

            if message is None:
                raise Exception('ERROR! Phone should have said something by now!\n')

            message = message.decode('utf-8').strip()

            # If the function fails here it was going to be wrong anyway
            if message == "FTP_COMPLETED":
                print("Success! The phone footage has finished transferring!\n")
                return

            if message == "ILLEGAL":
                raise Exception("ERROR! Phone sent back an illegal response!\n")

            errorMsg = "ERROR! Response received is not anything we expected! Recieved: " + message + "\n"
            raise Exception(errorMsg)

        except Exception as e:
            self.closeConn()
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

def main():
    test = PhoneControl(8000)
    test.sync()
    test.startRecording()
    test.stopRecording()

    test.startFileTransfer("Yeet/Street/Killem/StraightUp/Hee\ Hee")
    test.waitForFileTransfer()

    test.closeConn()

if __name__ ==  '__main__':
    main()

