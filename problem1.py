import json

def load_automaton(file_path):
    with open(file_path, 'r') as file:
        automaton = json.load(file)
    return automaton

def create_transition_function(transitions):
    transition_function = {}
    for (q, a, q_prime) in transitions:
        if (q, a) not in transition_function:
            transition_function[(q, a)] = q_prime
    return transition_function

def transition(q, a, δ):
    return δ.get((q, a), None)

def final_state(q, w, δ):
    for symbol in w:
        q = transition(q, symbol, δ)
        if q is None:
            return None
    return q

def derivation(q, w, δ):
    sequence = [q]  
    for symbol in w:
        next_q = transition(q, symbol, δ)
        if next_q is None:
            break
        sequence.append((symbol, next_q))
        q = next_q
    return sequence

def accepted(q, w, F, δ):
    final_q = final_state(q, w, δ)
    return final_q in F if final_q is not None else False

def format_derivation(derivation_seq):
    formatted = []
    for i in range(1, len(derivation_seq)):
        prev_state = derivation_seq[i-1] if isinstance(derivation_seq[i-1], str) else derivation_seq[i-1][1]
        symbol, next_state = derivation_seq[i]
        formatted.append(f"{prev_state} --{symbol}--> {next_state}")
    return ', '.join(formatted)

def main():
    print('\nLaboratorio 02 - Teoría de la Computación - Problema 01')
    automaton_files = ['automata1.json', 'automata2.json']
    print("\nAutómatas disponibles:")
    for i, file in enumerate(automaton_files):
        print(f"\t{i + 1}. {file}")

    while True:
        choice = input("\nIngrese el número del autómata que desea usar (1 o 2): ")
        if choice in ["1", "2"]:
            choice = int(choice) - 1
            break
        else:
            print("¡Opción inválida! Por favor, seleccione 1 o 2.")

    automaton = load_automaton(automaton_files[choice])

    Q = automaton['Q']
    alphabet = automaton['alphabet']
    q0 = automaton['initial_state']
    F = automaton['accepting_states']
    transitions = automaton['transitions']

    print(f"\nAlfabeto aceptado por el autómata seleccionado: {', '.join(alphabet)}")

    transition_function = create_transition_function(transitions)

    w = input("\nIngrese la cadena de entrada: ")

    final_q = final_state(q0, w, transition_function)
    derivation_seq = derivation(q0, w, transition_function)
    is_accepted = accepted(q0, w, F, transition_function)

    formatted_derivation = format_derivation(derivation_seq)

    print("\nResultados obtenidos:")
    print(f"\tEstado final: {final_q}")
    print(f"\tDerivación: {formatted_derivation}")
    if is_accepted:
        print(f"\tCadena aceptada: Sí es aceptado.\n")
    else:
        print(f"\tCadena aceptada: No, para que llegue al estado de aceptación tiene que llegar a {F}.\n")

if __name__ == "__main__":
    main()
