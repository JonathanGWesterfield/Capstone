

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
        self.connected = True

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

        return message



def main():
    """
    This main loop will run forever or until the RPI is manually killed.
    If the user sends the DISCONNECT command, we will disconnect but essentially start again so
    we can reconnect. The only time this program really dies is when the user throws a keyboard
    interrupt or shuts down the RPi
    :return: None
    """
    while(True):
        server = ServerRPi()
        stop = false
        while (True):
            message = server.listen()  # wait until we get a response from the laptop
            if message == 'FLASH':
                pass  # TODO: PUT THE FUNCTION TO FLASH THE LIGHT HERE
            elif message == 'DISCONNECT':
                stop = True

if __name__ ==  '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\nQuitting!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

