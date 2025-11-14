from dataclasses import dataclass
from status_code import STATUS_CODE
from typing import List 
from sdec import terminalData, command_list
import time
import threading

OPCODE = 0x01

@dataclass
class NodeData:
    command: str
    desc: str = ""

class Node:
    def __init__(self, node: NodeData, time_allowed: float | None, serialObj: terminalData):
        # Declare metadata
        self.command = node.command
        self.time_allowed = time_allowed 
        self.desc = node.desc
        self.status = STATUS_CODE.NEW
        # Serial object to handle serial comm
        self.serial = serialObj

        # Time
        self.elapsed = -1;

        # multithreading safe
        self.mutex = threading.Lock()

    """
    Get status of the node -> STATUS CODE
    Can be called when node is running
    """
    def get_status(self):
        return self.status

    """
    Get waiting time -> float, -1 means task hasn't started yet
    Can be called when node is running
    """
    def get_time_elapsed(self):
        return self.elapsed

    """
    Private function: send command using SDEC terminal object
    """
    def _send_command(self):
        if not self.serial.is_active():
            self.status = STATUS_CODE.CRITICAL
            return
        self.status = STATUS_CODE.IN_PROGRESS
        userin = self.command.strip().split()
        userCommand = userin[0]
        commandArgs = userin[1:]
        self.serial = command_list[userCommand](commandArgs, self.serial)
    
    """
    Private function: wait for response from hardware, timeout if it exceeds time allowed
    """
    def _wait_for_ack(self):
        start_time = time.time()
        while (True):
            if not self.serial.is_active():
                self.status = STATUS_CODE.CRITICAL
                return;

            if (self.time_allowed and self.elapsed >= self.time_allowed):
                self.status = STATUS_CODE.TIMEOUT
                return;

            resp_code = self.serial.readByte()
            if resp_code == OPCODE:
                self.status = STATUS_CODE.READY
                return;

            self.elapsed = time.time() - start_time

    """
    Run node
    """
    def run(self):
        self.mutex.acquire()
        self._send_command()
        self._wait_for_ack()
        self.mutex.release()
