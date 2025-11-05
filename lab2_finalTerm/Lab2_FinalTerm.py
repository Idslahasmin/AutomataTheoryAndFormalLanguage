# Final-Lab02 Solution (cleaned labels)
# Converts given Mealy machine to equivalent Moore machine,
# runs test inputs, prints results, and generates DOT graph files for diagrams.

from collections import defaultdict
from pathlib import Path

# -----------------------------
# Mealy transition table (from lab)
# -----------------------------
mealy_transitions = {
    'A': {'0': ('A', 'A'), '1': ('B', 'B')},
    'B': {'0': ('C', 'A'), '1': ('D', 'B')},
    'C': {'0': ('D', 'C'), '1': ('B', 'B')},
    'D': {'0': ('B', 'B'), '1': ('C', 'C')},
    'E': {'0': ('D', 'C'), '1': ('E', 'C')},
}
start_state = 'A'

# -----------------------------
# Run Mealy machine
# -----------------------------
def run_mealy(trans, start, input_str):
    s = start
    out = []
    for ch in input_str:
        ns, o = trans[s][ch]
        out.append(o)
        s = ns
    return ''.join(out)

# -----------------------------
# Convert Mealy → Moore
# -----------------------------
def convert_mealy_to_moore(mealy, start_state):
    moore_states = set()
    for p in mealy:
        for a, (q, o) in mealy[p].items():
            moore_states.add((q, o))
    # Name Moore states as "A/A", "B/B", etc.
    moore_name = {pair: f"{pair[0]}/{pair[1]}" for pair in moore_states}
    moore_output = {moore_name[pair]: pair[1] for pair in moore_states}

    moore_trans = defaultdict(dict)
    for (p, op) in moore_states:
        ms = moore_name[(p, op)]
        for symbol in mealy[p]:
            q, out_q = mealy[p][symbol]
            moore_trans[ms][symbol] = moore_name[(q, out_q)]

    # Initial Moore state
    first_symbol = next(iter(mealy[start_state].keys()))
    first_output = mealy[start_state][first_symbol][1]
    initial_moore = moore_name[(start_state, first_output)]

    return {
        'states': list(moore_name.values()),
        'start_state': initial_moore,
        'transitions': dict(moore_trans),
        'output_map': moore_output,
    }

# -----------------------------
# Run Moore machine
# -----------------------------
def run_moore(moore, input_str):
    s = moore['start_state']
    outputs = [moore['output_map'][s]]  # Moore emits output on entry
    for ch in input_str:
        s = moore['transitions'][s][ch]
        outputs.append(moore['output_map'][s])
    return ''.join(outputs)

# -----------------------------
# DOT exporters for diagrams
# -----------------------------
def mealy_to_dot(mealy, start, filename='mealy.dot'):
    lines = ['digraph Mealy {', 'rankdir=LR;', 'node [shape=circle];']
    lines.append(f'// start: {start}')
    for s in mealy:
        for a, (ns, o) in mealy[s].items():
            lines.append(f'  "{s}" -> "{ns}" [label="{a}/{o}"];')
    lines.append('}')
    Path(filename).write_text('\n'.join(lines))
    print(f"Mealy DOT written to {filename}")

def moore_to_dot(moore, filename='moore.dot'):
    lines = ['digraph Moore {', 'rankdir=LR;', 'node [shape=circle];']
    for st in moore['states']:
        lines.append(f'  "{st}" [label="{st}"];')
    lines.append(f'// start: {moore["start_state"]}')
    for s, trans in moore['transitions'].items():
        for a, ns in trans.items():
            lines.append(f'  "{s}" -> "{ns}" [label="{a}"];')
    lines.append('}')
    Path(filename).write_text('\n'.join(lines))
    print(f"Moore DOT written to {filename}")

# -----------------------------
# Main Execution
# -----------------------------
if __name__ == '__main__':
    moore = convert_mealy_to_moore(mealy_transitions, start_state)

    print("Moore machine states:", moore['states'])
    print("Moore outputs (per state):", moore['output_map'])
    print("Start state:", moore['start_state'])

    # Test input strings (from lab)
    test_inputs = ['00110', '11001', '1010110', '101111']
    print("\n==========================================================")
    print("{:<10} {:<15} {:<15} {:<15}".format("Input", "Mealy Output", "Moore Raw", "Moore Aligned"))
    print("==========================================================")

    for inp in test_inputs:
        mealy_out = run_mealy(mealy_transitions, start_state, inp)
        moore_out = run_moore(moore, inp)
        aligned = moore_out[1:]  # Drop initial output to align
        print("{:<10} {:<15} {:<15} {:<15}".format(inp, mealy_out, moore_out, aligned))

    print("==========================================================")

    # Save DOT files
    mealy_to_dot(mealy_transitions, start_state, 'mealy.dot')
    moore_to_dot(moore, 'moore.dot')
    print("\nDOT files generated: mealy.dot, moore.dot")
    print("Render with: dot -Tpng mealy.dot -o mealy.png | dot -Tpng moore.dot -o moore.png")
