from typing import List, Dict, Set, Tuple

lambda_ = 'λ'


class State:
    def __init__(self, q):
        self.q = q

    def __eq__(self, other):
        return self.q == other.q

    def __hash__(self):
        return 1


class Transition:
    def __init__(self, q_start: State, agent: str, q_final: State):
        self.q_start = q_start
        self.agent = agent
        self.q_final = q_final


class NFA:
    def __init__(self, alph: List[str], Q: List[State], q0: State, qf: List[State], transition_fun: Dict[Tuple[State,str],Set[State]]):
        self.alph = alph
        self.Q = Q
        self.q0 = q0
        self.qf = qf
        self.transition_fun = transition_fun


def convert_NFA_to_DFA(alphabet:List[str], states:List[State], q0:List[State], qf:List[State], transition_fun:Dict[Tuple[State, str], Set[State]]):
    """
    :param alphabet: list of the input symbols
    :param states: list of states
    :param q0: initial state
    :param qf: final state
    :param transition_fun: transition function that maps a state and an input symbol to a set of states
    :return: a DFA that accepts the same language as the NFA
    """
    # Initialize the DFA states and transitions
    dfa_states = []
    dfa_transitions = {}
    queue = []
    # Initialize the queue with the initial state
    for q0_mem in q0:
        queue.append(frozenset([q0_mem]))
        # Create the initial state of the DFA
        dfa_states.append(frozenset([q0_mem]))

    # Loop until the queue is empty
    while queue:
        # Get the next state from the queue
        current_state = queue.pop(0)

        # Loop over the input symbols
        for symbol in alphabet:
            # Compute the next state of the NFA
            next_state = set()
            for state in current_state:
                try:
                    next_state |= transition_fun[state, symbol]
                except KeyError:
                    next_state = set()

            # If the next state is not empty
            if next_state:
                # Convert the next state to a frozenset
                next_state = frozenset(next_state)

                # Add the next state to the DFA states if it is not already there
                if next_state not in dfa_states:
                    dfa_states.append(next_state)
                    queue.append(next_state)

                # Add the transition to the DFA transitions
                dfa_transitions[(current_state, symbol)] = next_state

    # Create the set of final states of the DFA

    # Create the set of final states of the DFA
    dfa_final_states = set()
    for state in dfa_states:
        for final in qf:
            if final in state:
                dfa_final_states.add(state)

    # Return the DFA
    return alphabet, dfa_states, q0, dfa_final_states, dfa_transitions


def find_lambda_transition(transitions: Dict[Tuple[State, str], Set[State]]):
    lambda_transition: Dict[Tuple[State, str], Set[State]] =dict()  # q1 lambda -> q2 , q1 lambda -> q3
    for (state, agent), final_state in transitions.items():
        if agent == lambda_:
            lambda_transition[state, agent] = final_state

    for (q_start, agent), q_final in lambda_transition.items():  # q1 -> {q2,q3} by lambda
        if q_start in lambda_transition.keys():
            prev_final_state = lambda_transition[q_start, agent]
            prev_final_state.update(q_final)
        else:
            lambda_transition[q_start, agent] = q_final

    return chain_of_lambda_rules(lambda_transition)

def chain_of_lambda_rules(dict_lambda_state:Dict[Tuple[State, str], Set[State]]):
    change = 1
    while change:
        change = 0
        for (start_state,agent), final_states in dict_lambda_state.items():
            new_final_states = set()
            new_final_states.update(final_states)
            for f in final_states:
                if f in dict_lambda_state.keys():  # q1-> q2 and q2->q3 => q1->q2,q3 and q2->q3
                    prev_states = dict_lambda_state[f, agent]
                    new_final_states.extend(prev_states)
                    new_final_states = list(set(new_final_states))
                    if final_states == new_final_states:
                        change += 1  # Convergence has happened
            dict_lambda_state[start_state, agent] = new_final_states
        if change == len(dict_lambda_state.keys()):  # reject convergence
            change = 0
    return dict_lambda_state

def define_initial_and_final_state(lambda_transition, transition_of_NFA ,q0, qf):
    new_initial_state = [q0]
    new_final_state = qf
    for (state, agent) , final_state in lambda_transition.items():
        if state.q == q0.q:
            for f in final_state:
                new_initial_state.append(f)
        if state in qf:
            for f in final_state:
                new_final_state.append(f)
    return new_initial_state , new_final_state
def delete_lambda_transition(transition_of_NFA, lambda_transition, alphabet):
    for (state, lambda__), final_states in lambda_transition.items():
        for final_s in final_states:
            for symbol in alphabet:
                try:
                    result = transition_of_NFA[final_s, symbol]
                    try:
                        prev_result = transition_of_NFA[state,symbol]
                        prev_result.update(result)
                    except KeyError:
                        transition_of_NFA[state, symbol] = result
                except KeyError:
                    pass

    for (state, lambda__), final_states in lambda_transition.items():
        try:
            del transition_of_NFA[state, lambda__]
        except KeyError:
            pass

    return transition_of_NFA

def process_of_lambda_transition(transition_of_NFA, q0, qf, alphabet):
    lambda_transition = find_lambda_transition(transition_of_NFA)
    new_initial_state, new_final_state = define_initial_and_final_state(lambda_transition, transition_of_NFA, q0, qf)
    transition_of_NFA = delete_lambda_transition(transition_of_NFA, lambda_transition, alphabet)
    return new_initial_state, new_final_state, transition_of_NFA


def read_file():
    with open("NFA2.txt") as fp:
        Lines = fp.readlines()
        count = 1
        alphabet: List[str] = []
        states: List[State] = []
        q0 = None
        qf: List[State] = []
        transition_fun: List[Transition] = []
        for line in Lines:
            if count == 1:  # Alphabet of language
                alphabet = line.strip().split()
            elif count == 2:  # states of automata
                str_states = line.strip().split()
                for q in str_states:
                    states.append(State(q))
            elif count == 3:  # first state
                q0 = State(line.strip())
            elif count == 4:  # final state
                str_final_states = line.strip().split()
                for q in str_final_states:
                    qf.append(State(q))
            elif count > 4:  # transition function
                transition_line = line.strip().split()
                parts = []
                for part in transition_line:
                    parts.append(part)
                transition_fun.append(Transition(State(parts[0]), parts[1], State(parts[2])))
            count += 1
        return alphabet, states, q0, qf, transition_fun


def dict_transitions(transition_fun):
    dict_transition: Dict[Tuple[State, str], Set[State]] = dict()
    for transition in transition_fun:
        q_start = transition.q_start
        agent = transition.agent
        q_final = transition.q_final
        if (q_start, agent) in dict_transition:
            prev_final_states = dict_transition[q_start, agent]
            prev_final_states.add(q_final)
        else:
            dict_transition[q_start, agent] = {q_final}
    return dict_transition




alphabet, states, q0, qf, transition_fun = read_file()
transition_of_NFA = dict_transitions(transition_fun)
new_initial_state, new_final_state, transition_of_NFA = process_of_lambda_transition(transition_of_NFA, q0, qf, alphabet)

for (state, agent), final_state in transition_of_NFA.items():
    print(f'{state.q} by agent {agent} got to {final_state}')
    for f in final_state:
        print(f.q)
    print("--------------------------")

DFA_alphabet, dfa_states, DFA_q0, dfa_final_states, DFA_transition = convert_NFA_to_DFA(alphabet, states, new_initial_state, new_final_state, transition_of_NFA)
print(f'DFA_alphabet : {DFA_alphabet}\n'
      f'initial_state: {DFA_q0}\n'
      f'final_state : {dfa_final_states}\n')
print("==================")
print(DFA_transition)