from typing import List, Set, Dict

class State:
    def __init__(self, q):
        self.q = q

    def __eq__(self, other):
        return self.q == other.q


class Transition:
    def __init__(self, q_start: State, agent: str, q_final: State):
        self.q_start = q_start
        self.agent = agent
        self.q_final = q_final


class DAF:
    def __init__(self, alph: List[str], Q: List[State],q0: State, qf: List[State], transition_fun: List[Transition]):
        self.alph = alph
        self.Q = Q
        self.q0 = q0
        self.qf = qf
        self.transition_fun = transition_fun

    def acceptor(self, input_):
        list_input = list(input_)
        current_q = self.q0
        for char in list_input:
            for rule in self.transition_fun:
                if rule.q_start == current_q and rule.agent == char:
                    current_q = rule.q_final
                    break

        if current_q in self.qf:
            return True
        return False


with open("DFA_Input_1.txt") as fp:
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

my_DFA = DAF(alphabet, states, q0, qf, transition_fun)
user_input = input("Enter string :")
result = my_DFA.acceptor(user_input)
print(result)

