#!/usr/bin/env python3

import socket
import datetime
# from Signal import Signals
import sys
import os

class Server:
    """
    This class was created to help me with testing the network functionality of the android phones so
    we can make sure the phones are behaving as intended.
    """

    def __init__(self, portNum: int):
        """
        Class constructor
        :param portNum: The port this server will be listening on
        """
        self.portNum = portNum
        self.host = ""
        self.connected = False

        self.socket = self.setupSocket()
        self.sync()

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
        self.socket.close()
        self.connected = False

    def sync(self):
        """
        Wait for the phone to make a connection.
        :return: None
        """
        self.conn, self.addr = self.socket.accept()
        self.connected = True
        print('Connection Found!\n')

    def sendCommand(self, message: str):
        """
        Function to help us send commands to the other end of the connection.
        :param message: The message we want to send
        :return: None
        """

        if self.conn is None:
            print("ERROR! NEED TO CONNECT TO PHONE FIRST")
            return

        command = bytes((message + "\n"), 'utf-8')  # need the '\n' char or the connection will hang

        self.conn.sendall(command)

        # Wait for the acknowledgement
        message = self.conn.recv(1024)

        if message is None:
            raise Exception('ERROR! Phone should have said something by now!\n')

        message = message.decode('utf-8').strip()

        print("Returned: ", message)


def main():
    """
    Take user input for what to send to the server until user kills the program
    :return: None
    """
    server = Server(8000)

    while(True):
        server.sendCommand(input("Send: "))

if __name__ ==  '__main__':
    main()
