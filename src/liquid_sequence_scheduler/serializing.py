import struct
import zlib
from dataclasses import dataclass, field
from typing import List

from src.liquid_sequence_scheduler.classes import SequenceNode, Hardware, Command
from src.liquid_sequence_scheduler.presets import engine_hardware

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
    
    def _bytes_as_hex_escape(self, b: bytes) -> str:
        return 'b"' + ''.join(f'\\x{byte:02x}' for byte in b) + '"'

    def __str__(self):
        packed_bytes = self.pack_to_bytes()
        return (
            f"Time: {self._bytes_as_hex_escape(packed_bytes[0:2])}\n" +
            f"Subcommand code: {self._bytes_as_hex_escape(packed_bytes[2:3])}\n" +
            f"Opcode: {self._bytes_as_hex_escape(packed_bytes[3:4])}\n" +
            f"Sequence Number: {self._bytes_as_hex_escape(packed_bytes[4:5])}\n" +
            f"CRC32: {self._bytes_as_hex_escape(packed_bytes[5:])}\n"
        )

def get_subcommand_code(parameter: Hardware | Command) -> int:
    if parameter.name in engine_hardware:
        match engine_hardware[parameter.name]:
            case "solenoid": return 81
            case "valve": return 82

            # default
            case _: return 0
    else:
        # TODO engine command code
        return 0

def get_opcode(parameter: Hardware | Command, switch: bool) -> int:
    match parameter.name:
        # solenoids
        case "oxpress": return 1 if switch else 9
        case "fuelpress": return 2 if switch else 16
        case "oxvent": return 3 if switch else 17
        case "fuelvent": return 4 if switch else 18
        case "oxpurge": return 5 if switch else 19
        case "fuelpurge": return 6 if switch else 20

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