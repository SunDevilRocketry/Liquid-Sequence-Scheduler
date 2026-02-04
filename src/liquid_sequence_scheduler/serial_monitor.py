import logging
import serial

from src.liquid_sequence_scheduler import serializing

def receive_serial_nodes(port: str, num_nodes: int):
    rcv_logger = logging.getLogger("serial.rcv")

    serial_connection = serial.Serial(
        port=port, # Paired with COM froom main.py
        baudrate=921600, # Matched with SDEC
        timeout=5,
        rtscts=False,
        xonxoff=False,
        dsrdtr=False,
    )
    if serial_connection.is_open: serial_connection.close() 
    serial_connection.open()

    for _ in range(num_nodes):
        rcv_node_data = serial_connection.read(9) # Read the 9 bytes of a node

        # Recreate SerialNode object for simple verification and printing
        rcv_node = serializing.SerialNode.from_bytes(
            data=rcv_node_data
        )
        rcv_logger.info(rcv_node)

    serial_connection.close()