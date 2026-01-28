import struct
import serial
import zlib
from dataclasses import dataclass, field
from typing import List

from classes import SequenceNode, Hardware, Command

@dataclass(frozen=True)
class SerialNode:
    time: bytes # 16 bits
    opcode: bytes # 8 bits
    sequence_num: bytes # 8 bits
    crc: bytes = field(init=False) # 32 bits

    def __post_init__(self):
        payload = b"".join([
            struct.pack(">e", self.time),
            struct.pack(">B", self.opcode),
            struct.pack(">B", self.sequence_num)
        ])

        object.__setattr__(self, "crc", zlib.crc32(payload) & 0xFFFF) 

    def pack_to_bytes(self) -> bytes:
        return b"".join([
            struct.pack(">e", self.time),
            struct.pack(">B", self.opcode),
            struct.pack(">B", self.sequence_num),
            struct.pack(">I", self.crc)
        ])
    
def float_to_time(value: float) -> bytes:
    return struct.pack(">e", value)

def parameter_to_opcode(parameter: Hardware | Command, switch: bool) -> bytes:
    match parameter.name:
        case "ox": return b"\x04" if switch else b"\x06"
        case "fuel": return b"\x05" if switch else b"\x07"
        case _: return b"\x00"

def serialize_sequence(sequence: List[SequenceNode]):
    connection = serial.Serial(
        port="",
        baudrate=921600,
        timeout=5
    )
    connection.open()

    for node in sequence:
        new_event = SerialNode(
            time=float_to_time(node.time),
            opcode=parameter_to_opcode(node.parameter, node.switch),
            sequence_num=node.num.to_bytes(1, "big"),
        )
        connection.write(new_event.pack_to_bytes())
        connection.reset_input_buffer()