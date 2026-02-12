from liquid_sequence_scheduler.classes import Hardware, Command, SequenceLine, SyntaxCheck, SequenceNode
from liquid_sequence_scheduler.presets import engine_hardware, engine_commands, allowed_on_off
from typing import List

# Syntax error function for parse_CSV() can use to throw syntax errors
def syntax_error(line_no, message):
    print(f"Syntax Error <{message}> at line: {line_no} while parsing")
    exit(-1)

# Parse a given CSV file following the sample sheet rules
# Place each time and command in a list which is appended to the sequence list
def parse_CSV(file: str) -> List[SequenceLine]:
    sequence_commands = []
    line_no = 2

    with open(file, "r") as f:
        f.readline() # Consume first line 

        for line in f:
            start_char = line[0]
            if start_char != ",":
                if start_char.isdigit():
                    line = line.split(",")
                    time = float(line[0])
                    parameter, switch = line[1].split(" ")
                    new_line = SequenceLine(line=line_no, 
                                 time=time, 
                                 parameter=parameter.lower(), 
                                 switch=switch.lower())
                    sequence_commands.append(new_line)
                else:
                    syntax_error(line_no, "Unexpected Character: Commands start with digits")

            line_no += 1
    
    return sequence_commands

# Perform syntax checking on the parsed data
def syntax_checking(sequence_list: List[SequenceLine]) -> SyntaxCheck:
    command_no = 1
    prev_time = -1

    # Make sure first command given is the initial "0, sequencing ON"
    first_line = sequence_list[0]
    if first_line.time != 0:
        return SyntaxCheck(False, 0, "Sequencing ON command not at time 0")

    if first_line.parameter != "sequencing":
        return SyntaxCheck(False, 0, "First command not sequecning")
    
    if first_line.switch not in {"on", "1"}:
        return SyntaxCheck(False, 0, "First command prompt not ON")
    
    sequence_list = sequence_list[1:]
    for line in sequence_list:
        # Make sure the time sequence is strictly increasing or equal to
        if line.time < prev_time:
            return SyntaxCheck(False, command_no, "Non-Increasing Time Sequence")
        
        # Determine if command is a hardware access or a command
        if line.parameter in engine_hardware.keys():
            # Command is to control hardware
            if line.switch not in allowed_on_off or line.switch not in allowed_on_off:
                # ON or OFF prompt not provided
                return SyntaxCheck(False, command_no, "Hardware Access requires an ON or OFF")
        elif line.parameter in engine_commands:
            # Command is to send an engine command
            if line.switch not in {"on", "1"}:
                # ON prompt not provided
                return SyntaxCheck(False, command_no, "Command send requires an ON")
        else:
            # Command does not exist
            return SyntaxCheck(False, command_no, f"Hardware or Command '{line.parameter}' does not exist")

        command_no += 1
        prev_time = line.time

    # No syntax problems found
    return SyntaxCheck(True, 0, "")

# Format the parsed list into a better typed list
def format_sequence(sequence_list: List[SequenceLine]) -> List[SequenceNode]:
    sequence: List[SequenceNode] = []

    for i, line in enumerate(sequence_list):
        new_node = SequenceNode(
            num=i,
            time=line.time,
            parameter=Command(name=line.parameter) if line.parameter in engine_commands else Hardware(name=line.parameter),
            switch=line.switch in {"on", "1"}
        )
        sequence.append(new_node)

    return sequence

# Print the sequence dict with formatting 
def print_sequence(sequence: List[SequenceNode]) -> None:
    for node in sequence:
        print(f"{node.time:.2f} | Command: {node.num} | {node.parameter.name} | {node.switch}")