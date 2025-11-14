from dataclasses import dataclass
from typing import List
from node import NodeData, Node
from status_code import STATUS_CODE
import time
import threading


@dataclass
class EventData:
    time_exec: float 
    next_time_exec: float | None
    nodes: List[NodeData]


class Event:
    def __init__(self, event: EventData):
        pass

    """
    Wait until next 
    """ 
    def idle(self):
        pass

    def error_handler(self, code: STATUS_CODE):
        match code:
            case STATUS_CODE.CRITICAL:
                pass
            case STATUS_CODE.TIMEOUT:
                pass

