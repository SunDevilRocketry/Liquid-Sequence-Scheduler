import logging
import serial
import time
import threading

from src.liquid_sequence_scheduler import parsing
from src.liquid_sequence_scheduler import serializing
from src.liquid_sequence_scheduler.serial_monitor import receive_serial_nodes

def init_logging():
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    send_logger = logging.getLogger("serial.send")
    send_logger.setLevel(logging.INFO)
    send_logger.propagate = False
    send_handler = logging.FileHandler("logging/sent.log", mode="w")
    send_handler.setFormatter(formatter)
    send_logger.addHandler(send_handler)

    rcv_logger = logging.getLogger("serial.rcv")
    rcv_logger.setLevel(logging.INFO)
    rcv_logger.propagate = False
    rcv_handler = logging.FileHandler("logging/rcv.log", mode="w")
    rcv_handler.setFormatter(formatter)
    rcv_logger.addHandler(rcv_handler)

def main():
    init_logging()
    send_logger = logging.getLogger("serial.send")

    sequence_list = parsing.parse_CSV("example/example_sheet.csv")
    syntax_result = parsing.syntax_checking(sequence_list)
    
    if (not syntax_result.result):
        print(f"Syntax Error: <{syntax_result.message}> at command number: {syntax_result.line}")
        exit(-1)
    else:
        print("Syntax checking passed")
        sequence = parsing.format_sequence(sequence_list)
        parsing.print_sequence(sequence)

    serial_sequence = serializing.serialize_sequence(sequence=sequence)

    serial_connection = serial.Serial(
        port="COM4", # Paired with COM5
        baudrate=921600, # Matched with SDEC
        timeout=1,
        write_timeout=1,
        rtscts=False,
        xonxoff=False,
        dsrdtr=False,
    )

    if serial_connection.is_open: serial_connection.close() 
    serial_connection.open()

    # Monitor serial output from COM5 to verify 
    monitor_thread = threading.Thread(target=receive_serial_nodes, args=("COM5", len(serial_sequence)))
    monitor_thread.start()

    time.sleep(0.1) # Monitor thread needs time to open its port

    for node in serial_sequence:
        send_logger.info(node)
        serial_connection.write(node.pack_to_bytes())

    monitor_thread.join()
    serial_connection.close()

if __name__ == "__main__":
    main()
