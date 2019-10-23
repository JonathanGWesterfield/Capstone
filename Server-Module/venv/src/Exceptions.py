# import Exception

class RecordingNotStartedException(Exception):
    """
    This exception class is for alerting the user that the recording has not started and they
    are trying to access a function that requires the phone cameras to be rolling.
    """
    def __init__(self, message: str):
        Exception.__init__(self, message)

class TransferNotStartedException(Exception):
    """
    This exception class is for alerting the user that the file transfer process has not been
    started and any actions that depend on it will fail.
    """
    def __init__(self, message: str):
        Exception.__init__(self, message)

class PhonesNotSyncedException(Exception):
    """
    This exception is for when the user tries to perform an operation with the phones without actually
    syncing the phones first.
    """
    def __init__(self, message: str):
        Exception.__init__(self, message)