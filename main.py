from src.liquid_sequence_scheduler import parsing
from src.liquid_sequence_scheduler import serializing

def main():
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
    for node in serial_sequence:
        print(node)

    # TODO make a connection and send the sequence 

if __name__ == "__main__":
    main()
