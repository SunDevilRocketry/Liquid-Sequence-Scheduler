from liquid_sequence_scheduler.parsing import parse_CSV
from liquid_sequence_scheduler.parsing import syntax_checking

# Format the parsed list into a dict for serialization 
def format_as_dict(sequence_list):
    sequence_dict = {}

    for pair in sequence_list:
        time = pair[0]
        command = pair[1]

        if time in sequence_dict.keys():
            sequence_dict[time].append(command)
        else:
            sequence_dict[time] = [command]

    return sequence_dict

# Print the sequence dict with formatting 
def print_sequence(sequence_dict):
    times = sequence_dict.keys()
    for time in times:
        commands = sequence_dict[time]
        for command in commands:
            command = command.split(" ")
            hardware_or_command = command[0]
            on_or_off = command[1]

            print(str(time) + ": " + hardware_or_command + " " + on_or_off)

def main():
    sequence_list = parse_CSV("./example/example_sheet.csv")
    print(sequence_list)
    syntax_result = syntax_checking(sequence_list)
    if (not syntax_result[0]):
        print(f"Syntax Error: <{syntax_result[2]}> at command number: {syntax_result[1]}")
        exit(-1)
    else:
        print("Syntax checking passed")
        sequence_dict = format_as_dict(sequence_list)
        print_sequence(sequence_dict)

if __name__ == "__main__":
    main()