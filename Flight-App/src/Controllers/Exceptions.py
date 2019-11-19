# import Exception

class RecordingNotStartedException(Exception):
    """
    This exception class is for alerting the user that the recording has not started and they
    are trying to access a function that requires the phone cameras to be rolling.
    """
    def __init__(self, message: str):
        """
        Calls the base Python Exception class and provides it with the error message we want to display.

        :param message: The error message we want the exception to contain to help with figuring out why the
        exception be being thrown.
        """
        Exception.__init__(self, message)

class TransferNotStartedException(Exception):
    """
    This exception class is for alerting the user that the file transfer process has not been
    started and any actions that depend on it will fail.
    """
    def __init__(self, message: str):
        """
        Calls the base Python Exception class and provides it with the error message we want to display.

        :param message: The error message we want the exception to contain to help with figuring out why the
        exception be being thrown.
        """
        Exception.__init__(self, message)

class PhonesNotSyncedException(Exception):
    """
    This exception is for when the user tries to perform an operation with the phones without actually
    syncing the phones first.
    """
    def __init__(self, message: str):
        """
        Calls the base Python Exception class and provides it with the error message we want to display.

        :param message: The error message we want the exception to contain to help with figuring out why the
        exception be being thrown.
        """
        Exception.__init__(self, message)

class RPINotConnectedException(Exception):
    """
    This class is for letting us know that we had an issue connecting to the raspberry pi.
    """
    def __init__(self, message: str):
        """
        Calls the base Python Exception class and provides it with the error message we want to display.

        :param message: The error message we want the exception to contain to help with figuring out why the
        exception be being thrown.
        """
        Exception.__init__(self, message)

class FailedRPIFlashException(Exception):
    """
    This error is for letting us know that the RPI did not flash the light.
    """
    def __init__(self, message: str):
        """
        Calls the base Python Exception class and provides it with the error message we want to display.

        :param message: The error message we want the exception to contain to help with figuring out why the
        exception be being thrown.
        """
        Exception.__init__(self, message)

class FailedDisconnectException(Exception):
    """
    This error is for telling us that something went wrong when we tried to disconnect from the RPI.
    """
    def __init__(self, message: str):
        """
        Calls the base Python Exception class and provides it with the error message we want to display.

        :param message: The error message we want the exception to contain to help with figuring out why the
        exception be being thrown.
        """
        Exception.__init__(self, message)