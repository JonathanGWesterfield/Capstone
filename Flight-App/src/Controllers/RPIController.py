import sys
import os
import requests
from Controllers.Exceptions import RPINotConnectedException, FailedRPIFlashException, FailedDisconnectException

class RPIController:
    """
    This class is for sending HTTP requests to the webserver running on the raspberry pi.
    We need this for being able to flash the light, and kill the server when we are running it.
    This module is written to be plugged into the Flight Application GUI.
    """

    def __init__(self, serverHost: str, portNum: int):
        """
        Class constructor. Initializes the controller with the proper settings to make HTTP requests
        to the node server running on the Raspberry pi.

        :param serverHost: The ip address or domain name of the server (the Raspberry PI).
        :param portNum: The port number that the node server is listening on.
        """
        self.__host = 'http://' + serverHost.strip() + ":" + portNum
        self.__flashEndpoint = '/flash'
        self.__disconnectEndpoint = '/disconnect'

    def flash(self) -> bool:
        """
        Sends an http request to the server to flash the light that will sync up the footage.

        :raises FailedRPIFlashException: Throws this exception if the server didn't send back the acknowledgement signal we were expecting.
        :return: True if the server sent back the **FLASH_ACKNOWLEDGE** message, false otherwise.
        """
        r = requests.get(self.__host + self.__flashEndpoint)

        # make sure we get the correct response from the server
        if r.status_code == 200:
            if r.text == 'FLASH_ACKNOWLEDGE':
                return True

        raise FailedRPIFlashException("Raspberry Pi failed to send the correct Acknowledge signal!!")

        return False

    def disconnect(self) -> bool:
        """
        Sends an http request to the server to kill the server. Will be called whenever the Flight
        application is finished and killed.

        :raises FailedDisconnectException: Throws this exception if the server didn't send back the acknowledgement signal we were expecting.
        :return: True if the server is dead, false otherwise.
        """
        r = requests.get(self.__host + self.__disconnectEndpoint)

        # make sure we get the correct response from the server
        if r.status_code == 200:
            if r.text == 'DISCONNECT_ACKNOWLEDGE':
                return True

        raise FailedDisconnectException("Raspberry Pi failed to send the correct Acknowledge signal!!")

        return False


def main():
    """
    Main method used for testing.

    :return: None
    """
    control = RPIController('localhost', '9876')

    if (control.flash()):
        print("Flashed the light!")

    if (control.disconnect()):
        print("Disconnected!")


if __name__ == '__main__':
    main()