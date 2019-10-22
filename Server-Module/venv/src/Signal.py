from enum import Enum

class Signals(Enum):
    """
    This class holds all of the valid signals that can be sent between the laptop and the phone. This
    should mirror the Signal enumeration in the android phone project.
    """
    START = 0
    STOP = 1
    START_ACKNOWLEDGE = 2
    STOP_ACKNOWLEDGE = 3
    FTP_STARTED = 4
    FTP_COMPLETED = 5
    ILLEGAL = 6
    NULL = 7