from enum import Enum, auto

class STATUS_CODE(Enum):
    READY = 0,
    NEW = auto(),
    IN_PROGRESS = auto(),
    CRITICAL = auto(),
    TIMEOUT = auto()