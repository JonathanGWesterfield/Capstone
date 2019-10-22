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

        self.socket = self.setupSocket()

    def getConnectionStatus(self) -> bool:
        """
        The getter function for seeing if the phones synced or not.
        :return: True if they have been synced, false otherwise
        """
        return self.connected

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

        # self.testTrack(addr, conn)

    def startTracking(self):
        """
        Call this in order to send a signal to the phones that they need to start tracking.
        :return:
        """
        threads = list()

        try:
            for conn in self.connections:
                # Start a new thread and return its identifier
                x = threading.Thread(target=self.threadStartTracking, args=(conn,))
                threads.append(x)
                x.start()

            for index, thread in enumerate(threads):
                thread.join()
                print("Threads joined!")

        except Exception as e:
            self.closeConn()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)





    def threadStartTracking(self, conn: socket.socket):
        """
        This is a thread for sending the message to the phone to start tracking and then waiting for the
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

            raise Exception("ERROR! Response received is not anything we expected!")

        except Exception as e:
            self.closeConn()
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def testTrack(self, addr, conn):
        self.threadStartTracking(conn)


def main():
    test = PhoneControl(8000)
    test.sync()
    test.startTracking()
    test.closeConn()

if __name__ ==  '__main__':
    main()







