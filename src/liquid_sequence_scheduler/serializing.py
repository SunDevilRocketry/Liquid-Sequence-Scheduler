import struct
import zlib
from dataclasses import dataclass, field
from typing import List

from src.liquid_sequence_scheduler.classes import SequenceNode, Hardware, Command

@dataclass(frozen=True)
class SerialNode:
    time: float # 16 bits
    subcommand_code: int # 8 bits
    opcode: int # 8 bits
    sequence_num: int # 8 bits
    crc: bytes = field(init=False) # 32 bits

    def __post_init__(self):
        payload = b"".join([
            struct.pack(">e", self.time),
            struct.pack(">B", self.subcommand_code),
            struct.pack(">B", self.opcode),
            struct.pack(">B", self.sequence_num)
        ])

        object.__setattr__(self, "crc", zlib.crc32(payload) & 0xFFFF) 

    def pack_to_bytes(self) -> bytes:
        return b"".join([
            struct.pack(">e", self.time),
            struct.pack(">B", self.subcommand_code),
            struct.pack(">B", self.opcode),
            struct.pack(">B", self.sequence_num),
            struct.pack(">I", self.crc)
        ])

def get_subcommand_code(parameter: Hardware | Command) -> int:
    hardware_type = parameter.name
    match hardware_type:
        case "solenoid": return 81
        case "valve": return 82

        # default
        case _: return 0

def get_opcode(parameter: Hardware | Command, switch: bool) -> int:
    match parameter.name:
        # solenoids
        case "oxPress": return 1 if switch else 9
        case "fuelPress": return 2 if switch else 16
        case "oxVent": return 3 if switch else 17
        case "fuelVent": return 4 if switch else 18
        case "oxPurge": return 5 if switch else 19
        case "fuelPurge": return 6 if switch else 20

        # valves
        case "ox": return 4 if switch else 6
        case "fuel": return 5 if switch else 7

        # default
        case _: return 0

def serialize_sequence(sequence: List[SequenceNode]) -> List[SerialNode]:
    serial_nodes: List[SerialNode] = []
    for node in sequence:
        new_event = SerialNode(
            time=node.time,
            subcommand_code=get_subcommand_code(node.parameter),
            opcode=get_opcode(node.parameter, node.switch),
            sequence_num=node.num
        )
        serial_nodes.append(new_event)
    
    return serial_nodes