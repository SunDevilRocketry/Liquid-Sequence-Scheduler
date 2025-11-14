from dataclasses import dataclass
from event import EventData
from node import NodeData
from typing import List
from collections import OrderedDict

@dataclass
class EventRow:
    time_exec: float
    command: str

class CSequence:
    def __init__(self, rows: List[EventRow]):
        seq = OrderedDict()
        events = []
        for row in self.rows:
            time_exec = row.time_exec
            command = row.command
            if not seq[time_exec]: 
                seq[time_exec] = [] 
            seq[time_exec].append(command) 
        
        for time, cmds in seq.items():
            nodes = []
            for cmd in cmds:
                node = NodeData(cmd)
                nodes.append(node)
        
        # TODO: Compile a list of event data. Have a list of timekeys to track of current and next event

    