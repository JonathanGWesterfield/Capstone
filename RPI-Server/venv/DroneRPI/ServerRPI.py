import socket
import datetime
import sys
import os
import time

class ServerRPi:
    """
    This class is for the server that will run on the raspberry pi. It will connect to the laptop.
    """

    def __init__(self, portNum: int):
        """
        Initializes the server settings
        """
        self.portNum = portNum
        self.host = ""
        self.connected = False
        self.socket = self.setupSocket()
        self.connect()


    def synced(self) -> bool:
        """
        The getter function for seeing if we are connected or not.
        :return: True if we are connected to the laptop, false otherwise
        """
        return self.connected

    def setupSocket(self):
        """
        Creates the socket that we will use to listen for incoming connections
        :raises: OSError Will throw an os error if the socket was closed too recently. "Address already in use"
        :return: None
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.portNum))

        print("Socket binded to port: ", self.portNum)

        sock.listen(5)
        print("Socket is listening for connections")

        return sock

    def connect(self):
        """
        Listens for any connection from the laptop so we can start
        :return: None
        """
        self.conn, self.addr = self.socket.accept()
        # self.sendCommand('CONNECTED')
        self.connected = True

    def closeConn(self):
        """
        Closes all of the connections and the socket.
        :return: None
        """
        # Make sure the phones are connected and synced first
        if not self.connected:
            return

        self.socket.shutdown(2)
        self.socket.close()
        self.connected = False
        print("Connection closed")

    def sendCommand(self, message: str):
        """
        Function to help us send commands to the other end of the connection.
        :param message: The message we want to send
        :return: None
        """

        if self.conn is None:
            print("ERROR! NEED TO CONNECT TO LAPTOP FIRST")
            return

        command = bytes((message + "\n"), 'utf-8')  # need the '\n' char or the connection will hang

        self.conn.sendall(command)


    def listen(self):
        """
        Listens to the other side of the connection for any message that might get sent through.
        :return: The message that was received from the other side.
        """
        if self.conn is None:
            print("ERROR! NEED TO CONNECT TO LAPTOP FIRST")
            return

        print("Listening!\n")
        # Wait for the acknowledgement
        message = self.conn.recv(1024)

        if message is None:
            raise Exception('ERROR! Phone should have said something by now!\n')

        message = message.decode('utf-8').strip()

        if message == '':
            raise Exception('ERROR! Received empty String!')
        print("Received: ", message, "\n")

        return message

def main():
    """
    This main loop will run forever or until the RPI is manually killed.
    If the user sends the DISCONNECT command, we will disconnect and end the program. Being able to ssh into
    the RPI is essential.
    :return: None
    """
    try:
        server = ServerRPi(8001)
        stop = False
        while (not stop):
            message = server.listen()  # wait until we get a response from the laptop
            if message == 'FLASH':
                """
                TODO: PUT THE FUNCTION TO FLASH THE LIGHT HERE
                """
                server.sendCommand('FLASH_ACKNOWLEDGE')
            elif message == 'DISCONNECT':
                server.sendCommand('DISCONNECT_ACKNOWLEDGE')
                stop = True

        # If the inner loop is escaped, it means kill connection and start over
        print("Killing server")
        server.closeConn()
    except KeyboardInterrupt:
        print('\n\nQuitting!')
        try:
            server.closeConn()
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ ==  '__main__':
    main()

