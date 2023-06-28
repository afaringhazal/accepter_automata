# Define the Turing machine
def turing_machine(input):

    # Define the states
    states = {
        'q0': {'0': ('q5', '0', 'R'), '1': ('q1', 'X', 'R')},
        'q1': {'0': ('q2', '0', 'R'), '1': ('q1', '1', 'R')},
        'q2': {'X': ('q2', 'X', 'R'), '#': ('correct_ansAE', '#', 'L'), '1': ('q3', 'X', 'L')},
        'q3': {'X': ('q3', 'X', 'L'), '0': ('q4', '0', 'L')},
        'q4': {'X': ('q0', 'X', 'R'), '1': ('q4', '1', 'L')},
        'q5': {'X': ('q5', 'X', 'R'), '1': ('correct_ansB', '1', 'L'),'#':('correct_ansAE', '#','L')},
        'correct_ansAE': {'X': ('correct_ansAE', '1', 'L'), '1': ('correct_ansAE', '1', 'L'), '0': ('correct_ansAE', 0, 'L'), '#': ('start_the_next_machineAE', '#', 'R')},
        'correct_ansB': {'X': ('correct_ansB', '1', 'L'), '1': ('correct_ansB', '1', 'L'), '0': ('correct_ansB', 0, 'L'), '#': ('start_the_next_machineB', '#', 'R')}

    }

    # Initialize the tape with the input
    tape = list('#' + input + '#')

    # Initialize the head position and state
    head_pos = 1
    state = 'q0'

    # Define the transition function
    while state != 'start_the_next_machineAE' and state != 'start_the_next_machineB':
        # Read the current symbol
        symbol = tape[head_pos]

        # Get the transition rule for the current state and symbol
        try:
            next_state, write_symbol, direction = states[state][symbol]
        except KeyError:
            raise Exception(f"Invalid symbol '{symbol}' in state '{state}'")

        # Write the next symbol
        tape[head_pos] = write_symbol

        # Move the head in the next direction
        if direction == 'R':
            head_pos += 1
        elif direction == 'L':
            head_pos -= 1

        # Transition to the next state
        # if next_state == 'correct_ans' and first:
        #     first = 0
        #     print(state)
        #     print(write_symbol)

        state = next_state


    print("state :" + state)
    print(tape)
    return tape, state


# Call the Turing machine
input = "111011"
turing_machine(input)
# Print the result
# print(result)