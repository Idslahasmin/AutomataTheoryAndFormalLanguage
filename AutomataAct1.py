#1
def dfa_accepts_1(string):
    state = 'a'  # start state
    
    for symbol in string:
        if state == 'a':
            if symbol == 0:
                state = 'a'
            elif symbol == 1:
                state = 'b'
            else:
                return False
        elif state == 'b':
            if symbol == 0:
                state = 'end'
            elif symbol == 1:
                state = 'a'
            else:
                return False
        elif state == 'end':
            if symbol == 0:
                state = 'b'
            elif symbol == 1:
                state = 'end'
            else:
                return False
        else:
            return False
    
    accepting_states = {'end'}
    return state in accepting_states

#2
def dfa_accepts_2(string):
    state = 'q0'
    
    for symbol in string:
        if state == 'q0':
            if symbol == 'a':
                state = 'q1'
            elif symbol == 'b':
                state = 'q2'
            else:
                return False
        elif state == 'q1':
            if symbol == 'a':
                state = 'q0'
            elif symbol == 'b':
                state = 'q3'
            else:
                return False
        elif state == 'q2':
            if symbol == 'a':
                state = 'q3'
            elif symbol == 'b':
                state = 'q0'
            else:
                return False
        elif state == 'q3':
            if symbol == 'a':
                state = 'q2'
            elif symbol == 'b':
                state = 'q1'
            else:
                return False
        else:
            return False

    accepting_states = {'q0', 'q3'}
    return state in accepting_states

# Utility to test and print results
def test_dfa(dfa_func, accepted, rejected, label):
    print(f"\n=== Testing DFA {label} ===")
    print(f"{'Input':<20} {'Expected':<10} {'Result'}")
    print("-" * 45)

    for s in accepted:
        result = dfa_func(s)
        print(f"{str(s):<20} {'Accepted':<10} {'Accepted' if result else 'Rejected'}")

    for s in rejected:
        result = dfa_func(s)
        print(f"{str(s):<20} {'Rejected':<10} {'Accepted' if result else 'Rejected'}")

# Test cases
accepted_1 = [[0,1,0], [1,0,1], [0,1,0,1]]
rejected_1 = [[0,1,0,1,0], [1,0,0,1], [1,0,0,1,0]]

accepted_2 = [['a','b'], ['a','b','a','a'], ['a','b','a','b']]
rejected_2 = [['a','b','b'], ['a','b','a'], ['a','b','a','b','b']]

# Run tests
test_dfa(dfa_accepts_1, accepted_1, rejected_1, "Number 1")
test_dfa(dfa_accepts_2, accepted_2, rejected_2, "Number 2")
