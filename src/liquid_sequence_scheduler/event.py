from dataclasses import dataclass
from typing import List
from node import NodeData, Node
from status_code import STATUS_CODE
from sdec import terminalData
import time
import threading


@dataclass
class EventData:
    time_exec: float 
    next_time_exec: float | None
    nodes: List[NodeData]


class Event:
    def __init__(self, event: EventData, serialObj: terminalData):
        self.current_event_start_time = event.time_exec
        self.next_event_start_time = event.next_time_exec
        self.time_allowed = event.next_time_exec - event.time_exec
        assert(self.time_allowed < 0) # Super crit event, time must be in order, should never happen irl

        # Construct node threads
        self.node_threads, self.node_objs = self._construct_nodes(event.nodes, serialObj)

    """
    Construct threads and nodes
    """ 
    def _construct_nodes(self, nodes: List[NodeData], serialObj: terminalData) -> tuple[List[threading.Thread], List[Node]]:
        threads = []
        node_objs = []
        for node in nodes:
            n = Node(node, self.time_allowed, serialObj)
            node_objs.append(n)
            threads.append(threading.Thread(target= n.run))
        return threads, node_objs

    """
    Print thread status
    """ 
    def print_status(self):
        for node, idx in enumerate(self.node_objs):
            print(f"Node {idx} status: {node.get_status()} elapsed: {node.get_time_elapsed()}")
        print() # Breakline

    """
    Execute nodes
    """ 
    def execute_nodes(self):
        # Start execution
        start = time.time()
        for thread in self.node_threads:
            thread.start()

        while (True):
            # Check status
            code_sum = 0
            
            for node in self.node_objs:
                status_code = node.get_status()
                self.error_handler(status_code)
                code_sum += status_code.value

            if code_sum == 0:
                time_completed = time.time() - start
                wait_time = self.next_event_start_time - time_completed
                self.idle(wait_time)
                return     
        
    """
    Wait until next cycle
    """ 
    def idle(self, wait_time: float):
        time.sleep(wait_time)

    """
    Handle error when see error code
    """ 
    def error_handler(self, code: STATUS_CODE):
        #TODO: Add proper error handlers
        match code:
            case STATUS_CODE.CRITICAL:
                while (True):
                    print("CRITICAL")
            case STATUS_CODE.TIMEOUT:
                while (True):
                    print("TIMEOUT")

