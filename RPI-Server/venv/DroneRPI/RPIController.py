import socket
import datetime
# from Signal import Signals
import sys
import os
from RPIExceptions import RPINotConnectedException, FailedRPIFlashException, FailedDisconnectException

from _thread import *
import threading

class RpiController:
    """
    This class provides controls that the front end UI can call to connect to the RPI and flash the light.
    """

    def __init__(self, rpiIPAddr:str, portNum: int):
        """
        Initializes the server.
        :param rpiIPAddr: The ip address or domain name of the Raspberry pi
        :param portNum: The port number that we are going to connect to the RPI through.
        """
        self.portNum = portNum
        self.host = rpiIPAddr

        self.connect()

    def connect(self):
        """
        Setups up the connection to the pi. The pi should return back 'CONNECTED' if the connection
        is successful.
        :return:
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.bind(self.host, self.portNum)
        # print("Socket binded to port: ", self.portNum)

        self.socket.connect((self.host, self.portNum))

        self.socket.sendall(bytes("HELLO\n", 'utf-8'))

        # message = self.socket.recv(1024)
        #
        # if message is None:
        #     raise Exception('ERROR! Phone should have said something by now!\n')
        #
        # message = message.decode('utf-8').strip()
        #
        # if not (message == 'CONNECTED'):
        #     raise Exception(self, "SERVER SENT BACK AN ILLEGAL MESSAGE!")

        return

    def flashLight(self):
        """
        Sends the signal to the raspberry pi to activate and flash the light.
        :return: None
        """
        self.socket.sendall(bytes("FLASH\n", 'utf-8'))

        acknowledge = self.socket.recv(1024)

        if acknowledge is None:
            raise Exception('ERROR! Phone should have said something by now!\n')

        acknowledge = acknowledge.decode('utf-8').strip()

        if not (acknowledge == 'FLASH_ACKNOWLEDGE'):
            raise FailedRPIFlashException("Server did not acknowledge the flash signal!")

        print("Received Flash Acknowledgement")
        return

    def disconnect(self):
        """
        Sends the signal to the raspberry pi to disconnect and kill its server.
        :return: None
        """
        self.socket.sendall(bytes("DISCONNECT\n", 'utf-8'))
        acknowledge = self.socket.recv(1024)

        if acknowledge is None:
            raise Exception('ERROR! Phone should have said something by now!\n')

        acknowledge = acknowledge.decode('utf-8').strip()

        if not (acknowledge == "DISCONNECT_ACKNOWLEDGE"):
            raise FailedDisconnectException("The server failed to acknowledge our disconnect signal!")

        print("Recieved Disconnect Acknowledgement")

        self.socket.close()
        self.socket.shutdown()

def main():
    controller = RpiController('localhost', 8001)
    controller.connect()

    try:
        while(True):
            print("Commands: FLASH, DISCONNECT")
            command = input("Command: ")
            if command == 'FLASH':
                controller.flashLight()
            elif command == 'DISCONNECT':
                controller.disconnect()
    except KeyboardInterrupt:
        print('\n\nQuitting!')
        try:
            controller.disconnect()
            sys.exit(0)
        except SystemExit:
            os._exit(0)




if __name__ ==  '__main__':
    main()










