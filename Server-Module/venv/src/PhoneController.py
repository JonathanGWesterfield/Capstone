import socket
import datetime
from Signal import Signals
import sys
import os

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
        self.transferFlag = False

        self.socket = self.setupSocket()

    def synced(self) -> bool:
        """
        The getter function for seeing if the phones synced or not.
        :return: True if they have been synced, false otherwise
        """
        return self.connected

    def transferring(self) -> bool:
        """
        A flag for us to access to see if the system is still waiting for the video to finish the file
        transfer of the videos it recorded.
        :return: True if the video has finished transferring, false otherwise.
        """
        return self.transferFlag

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
        for conn in self.connections:
            conn.close()

        self.socket.close()

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

    def startRecording(self):
        """
        Call this in order to send a signal to the phones that they need to start recording.
        :return:
        """
        threads = list()

        try:
            for conn in self.connections:
                # Start a new thread and return its identifier
                x = threading.Thread(target=self.threadStartRecording, args=(conn,))
                threads.append(x)
                x.start()

            for index, thread in enumerate(threads):
                thread.join()
            print("Start Threads Joined!")

        except Exception as e:
            self.closeConn()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


    def threadStartRecording(self, conn: socket.socket):
        """
        This is a thread for sending the message to the phone to start recording and then waiting for the
        the phone to send back a response acknowledging it.
        :param conn: A socket connection that has already been opened.
        :return: None
        """
        try:
            # Send the start command to the phone
            timestamp = datetime.datetime.now()
            command = bytes(("START-" + str(timestamp) + "\n"), 'utf-8')

            print("Sending the Start Signal\n")
            conn.sendall(command)
            print("Start signal sent.\nWaiting for acknowledgment")

            # Wait for the start acknowledgement
            message = conn.recv(1024)

            if message is None:
                raise Exception('ERROR! Phone should have said something by now')

            message = message.decode('utf-8').strip()

            # If the function fails here it was going to be wrong anyway
            if message == "START_ACKNOWLEDGE":
                print("Success! The phone acknowledged the start command")
                return

            if message == "ILLEGAL":
                raise Exception("ERROR! Phone sent back an illegal response")

            errorMsg = "ERROR! Response received is not anything we expected! Recieved: " + message
            raise Exception(errorMsg)

        except Exception as e:
            self.closeConn()
            print(e)
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
        threads = list()

        try:
            for conn in self.connections:
                # Start a new thread and return its identifier
                x = threading.Thread(target=self.threadStopRecording, args=(conn,))
                threads.append(x)
                x.start()

            for index, thread in enumerate(threads):
                thread.join()
            print("Stop Threads Joined!")

        except Exception as e:
            self.closeConn()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def threadSendSignal(self,conn: socket.socket, signal: str, sigMessage: str, sigAck: str):
        """
        This function takes a signal and the expected output so that we don't have to rewrite the same code for
        every action we have with the phones.
        :param signal: The Signal we want to send to the phone. Valid options are: START, STOP, and START_FTP
        :param sigMessage: A message that we want to send alongside the signal for the phone to use.
        :param sigAck: The Signal we expect to get back from the phone in response to our signal. Valid options
            are: START_ACKNOWLEDGE, STOP_ACKNOWLEDGE, START_FTP_ACKNOWLEDGE
        :param conn: A socket connection to a phone that has already been opened.
        :return: None
        """
        try:
            # Send the stop command to the phone
            timestamp = datetime.datetime.now()
            command = bytes((signal + "-" + sigMessage + "\n"), 'utf-8') # need the '\n' char or the connection will hang

            print("Sending the " + signal + " Signal\n")
            conn.sendall(command)
            print(signal + " signal sent.\nWaiting for acknowledgment")

            # Wait for the start acknowledgement
            message = conn.recv(1024)

            if message is None:
                raise Exception('ERROR! Phone should have said something by now')

            message = message.decode('utf-8').strip()

            # If the function fails here it was going to be wrong anyway
            if message == sigAck:
                print("Success! The phone acknowledged the " + signal + " command")
                return

            if message == "ILLEGAL":
                raise Exception("ERROR! Phone sent back an illegal response")

            errorMsg = "ERROR! Response received is not anything we expected! Recieved: " + message
            raise Exception(errorMsg)

        except Exception as e:
            self.closeConn()
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def threadStopRecording(self, conn: socket.socket):
        """
        This is a thread for sending the message to the phone to stop recording and then waiting for the
        the phone to send back a response acknowledging it.
        :param conn: A socket connection to a phone that has already been opened.
        :return:
        """
        try:
            # Send the stop command to the phone
            timestamp = datetime.datetime.now()
            command = bytes(("STOP-" + str(timestamp) + "\n"), 'utf-8') # need the '\n' char or the connection will hang

            print("Sending the Stop Signal\n")
            conn.sendall(command)
            print("Stop signal sent.\nWaiting for acknowledgment")

            # Wait for the start acknowledgement
            message = conn.recv(1024)

            if message is None:
                raise Exception('ERROR! Phone should have said something by now')

            message = message.decode('utf-8').strip()

            # If the function fails here it was going to be wrong anyway
            if message == "STOP_ACKNOWLEDGE":
                print("Success! The phone acknowledged the stop command")
                return

            if message == "ILLEGAL":
                raise Exception("ERROR! Phone sent back an illegal response")

            errorMsg = "ERROR! Response received is not anything we expected! Recieved: " + message
            raise Exception(errorMsg)

        except Exception as e:
            self.closeConn()
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    # def startFileTransfer(self, filepath: str):
    #     """
    #     Will send a signal to the phone that tells it to transfer the video files it recorded over to the laptop
    #     by opening an FTP connection.
    #     :param filepath: The file path on our laptop that the phones will need to send their videos to over FTP.
    #     :return: None
    #     """
    #     threads = list()
    #
    #     try:
    #         for conn in self.connections:
    #             # Start a new thread and return its identifier
    #             x = threading.Thread(target=self.threadStartFileTransfer, args=(conn, filepath))
    #             threads.append(x)
    #             x.start()
    #
    #         for index, thread in enumerate(threads):
    #             thread.join()
    #
    #         print("Start FTP Threads Joined!")
    #         self.transferFlag = True # Set flag that we are currently transferring the file over
    #
    #     except Exception as e:
    #         self.closeConn()
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #         print(exc_type, fname, exc_tb.tb_lineno)
    #
    #
    # def threadStartFileTransfer(self, filepath: str):
    #     """
    #     This is a thread for sending the message to the phone to start transferring the video and then waiting for the
    #     the phone to send back a response acknowledging it.
    #     :param filepath: The file path on our laptop that the phones will need to send their videos to over FTP.
    #     :return: None
    #     """
    #
    #
    # def waitForFileTransfer(self):
    #     """
    #     Spawns threads that will wait for both phones to send a signal saying that the file transfer
    #     of the videos is complete.
    #     :return: None
    #     """
    #
    # def threadWaitForFileTransfer(self):
    #     """
    #     This is a thread for waiting for the signal from the phone that the file transfer to the filepath specified
    #     in the startFileTransfer() function arguments.
    #     :return:
    #     """





def main():
    test = PhoneControl(8000)
    test.sync()
    test.startRecording()
    test.stopRecording()
    test.closeConn()

if __name__ ==  '__main__':
    main()







