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
    START_FTP = 4
    START_FTP_ACKNOWLEDGE = 5
    FTP_COMPLETED: Signals = 6
    ILLEGAL = 7
    NULL = 8