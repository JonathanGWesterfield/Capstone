class RPINotConnectedException(Exception):
    """
    This class is for letting us know that we had an issue connecting to the raspberry pi.
    """
    def __init__(self, message: str):
        Exception.__init__(self, message)

class FailedRPIFlashException(Exception):
    """
    This error is for letting us know that the RPI did not flash the light.
    """
    def __init__(self, message: str):
        Exception.__init__(self, message)

class FailedDisconnectException(Exception):
    """
    This error is for telling us that something went wrong when we tried to disconnect from the RPI.
    """
    def __init__(self, message: str):
        Exception.__init__(self, message)