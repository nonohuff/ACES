# imports
from generate_A import generate_A
from amatrixsolver import Amatrixsolve
from lambda_to_error import error
import numpy as np

import qiskit as qk
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
import random
from collections import Counter

from generator import generateCliffordCircuit

width = 5  # num_qubits
depth = 5  # number of layers in the circuit (easy + hard)
singleGateSet = ['X', 'H', 'Z', 'I', 'S']
doubleGateSet = ['CNOT_C', 'CNOT_T']

# Necessary functions
def makeNoisyGates(qiskitCir, whichQubits, px=0, py=0, pz=0):
    singleOrDouble = len(whichQubits)
    if singleOrDouble == 1:
        gateString = np.random.choice(['I', 'X', 'Y', 'Z'], p=[1-px-py-pz, px, py, pz])
        if gateString == 'I':
            qiskitCir.id(whichQubits[0])
        elif gateString == 'X':
            qiskitCir.x(whichQubits[0])
        elif gateString == 'Y':
            qiskitCir.y(whichQubits[0])
        elif gateString == 'Z':
            qiskitCir.z(whichQubits[0])
    else:
        gateString1 = np.random.choice(['I', 'X', 'Y', 'Z'], p=[1-px-py-pz, px, py, pz])
        if gateString1 == 'I':
            qiskitCir.id(whichQubits[0])
        elif gateString1 == 'X':
            qiskitCir.x(whichQubits[0])
        elif gateString1 == 'Y':
            qiskitCir.y(whichQubits[0])
        elif gateString1 == 'Z':
            qiskitCir.z(whichQubits[0])
        gateString2 = np.random.choice(['I', 'X', 'Y', 'Z'], p=[1-px-py-pz, px, py, pz])
        if gateString2 == 'I':
            qiskitCir.id(whichQubits[1])
        elif gateString2 == 'X':
            qiskitCir.x(whichQubits[1])
        elif gateString2 == 'Y':
            qiskitCir.y(whichQubits[1])
        elif gateString2 == 'Z':
            qiskitCir.z(whichQubits[1])
    return qiskitCir

def transpileListToQiskitCircuit(cir, noise=False, px=0, py=0, pz=0):
    depth = len(cir)
    width = len(cir[0])
    qiskitCir = QuantumCircuit(width)
    for d in range(depth):
        if d % 2 == 0:
            for w in range(width):
                singleGate = cir[d][w]
                stringToQiskitSingleGate(singleGate, qiskitCir, w)
            if noise:
                qiskitCir.barrier()
                for w in range(width):
                    makeNoisyGates(qiskitCir, [w], px, py, pz)
            if d != width - 1:
                qiskitCir.barrier()
        else:
            c = cir[d].index('CNOT_C')
            t = cir[d].index('CNOT_T')
            qiskitCir.cx(c, t)
            if noise:
                qiskitCir.barrier()
                makeNoisyGates(qiskitCir, [c, t], px, py, pz)
            if d != width - 1:
                qiskitCir.barrier()
    return qiskitCir

def stringToQiskitSingleGate(gateString, qiskitCir, whichQubit):
    if gateString == 'I':
        qiskitCir.id(whichQubit)
    elif gateString == 'X':
        qiskitCir.x(whichQubit)
    elif gateString == 'Y':
        qiskitCir.y(whichQubit)
    elif gateString == 'Z':
        qiskitCir.z(whichQubit)
    elif gateString == 'H':
        qiskitCir.h(whichQubit)
    elif gateString == 'S':
        qiskitCir.s(whichQubit)

def Clifford_Permute(cliff,pauli,qargs = None):
    '''This function permutes the pauli operators according to the clifford group, so it computes 
    P' = C P C^T, where C is a clifford operator and P is a pauli operator.
    Inputs: cliff - A Qiskit Circuit, Clifford, or Gate object.
            pauli - A Qiskit Pauli object.
    Outputs: new_pauli - A Qiskit Pauli object.'''

    if type(pauli) == qk.quantum_info.Pauli:
        input_pauli_string = ''.join(char for char in pauli.to_label() if char.isalpha())
        input_pauli_string = input_pauli_string[::-1]
        p = qk.quantum_info.Pauli(input_pauli_string)
    elif type(pauli) == str:
        input_pauli_string = ''.join(char for char in pauli if char.isalpha())
        input_pauli_string = input_pauli_string[::-1]
        p = qk.quantum_info.Pauli(input_pauli_string)

    return p.evolve(cliff,qargs,frame="s")

def split_circuit_by_barrier(circuit):
    qasm = circuit.qasm()
    prelude = []
    circuits = [[]]
    for line in qasm.splitlines():
        if any([line.startswith(t) for t in ['OPENQASM', 'include', 'qreg', 'creg']]):
            prelude.append(line)
        elif line.startswith('barrier'):
            circuits.append([])
        else:
            circuits[-1].append(line)
    circuits_with_prelude = [prelude+circuit for circuit in circuits]
    for circuit_with_prelude in circuits_with_prelude:
        yield qk.QuantumCircuit.from_qasm_str('\n'.join(circuit_with_prelude))

def G_twirling(circuit):
    '''This function performs G-twirling on a circuit. It randomly chooses a Pauli from {X,Y,Z,I} and prepends it before a layer, then appends P'=CPC^T after the layer.}
    Inputs: circuit - A Qiskit Circuit object.
    Outputs: new_circuit - A Qiskit Circuit object.'''
    num_qubits = circuit.num_qubits
    new_circuit = qk.QuantumCircuit(num_qubits)
    for index, subcircuit in enumerate(split_circuit_by_barrier(circuit)):
        # if len(subcircuit.data) == 1:
        #     operated_qubits = [subcircuit.find_bit(q).index for q in subcircuit.data[0].qubits]
        # else:
        #     operated_qubits = list(range(num_qubits))
        pauli_str = ''.join(random.choice(["X","Y","Z","I"]) for _ in range(num_qubits))
        pauli = qk.quantum_info.Pauli(pauli_str[::-1])
        new_circuit = new_circuit.compose(pauli,qubits=range(num_qubits))
        new_circuit = new_circuit.compose(subcircuit,qubits=range(num_qubits))
        new_circuit = new_circuit.compose(Clifford_Permute(subcircuit,pauli_str).to_instruction(),qubits = range(num_qubits))
        if index != len(list(split_circuit_by_barrier(circuit)))-1:
            new_circuit.barrier()
    return new_circuit


def random_choices_with_counts(items, n):
    """
    Randomly choose with replacement n items from a list and return a dictionary
    with the counts of each chosen item.
    
    Parameters:
        items (list): List of items to choose from.
        n (int): Number of items to choose.
    
    Returns:
        dict: Dictionary with the counts of each chosen item.
    """
    chosen_items = random.choices(items, k=n)
    counts = Counter(chosen_items)
    return dict(counts)

def find_circuit_from_name(circuit_list,target_name):
    # Find the circuit with the given name
    found_circuit = None
    for circuit in circuit_list:
        if circuit.name == target_name:
            found_circuit = circuit
            break

    # Check if the circuit was found
    if found_circuit is not None:
        # print(f"Circuit with name '{target_name}' found:")
        # print(found_circuit)
        return found_circuit
    else:
        print(f"No circuit with name '{target_name}' found.")
        return found_circuit
    
def prep_circuit(input_pauli):
    '''This function prepares the input state for eigenvalue sampling. It takes in a Pauli operator to be input into the circuit and outputs a circuit that prepares the state |psi+> or |psi-> from the input |0>^n, 
    where |psi+> and |psi-> are the eigenstates of the input Pauli operator.
    Inputs: input_pauli - A Qiskit Pauli object or a string representing a Pauli operator.
    Outputs: prep_circ - A Qiskit Circuit object which will prepare the state |psi+> or |psi-> from |0>^n, where |psi+> and |psi-> are the eigenstates of the input Pauli operator.
    '''
    # mapping for preparation circuit. The idea of the prep circuit is that we append it before the circuit to eigenvalue samp
    # i.e. input the state where all qubits are zero 1000...0> into the prep circuit and then input it's ouput into the circu
    # |0> -> ...
    # H -> |+>
    # XH -> |->
    # HS -> |+i>
    # XHS -> |-i>
    # I -> |0> (no change)
    # X -> |1>
    if type(input_pauli) == str:
        input_pauli_string = ''.join(char for char in input_pauli if char.isalpha()) # removes the phase from the Pauli string if present
    elif type(input_pauli) == qk.quantum_info.Pauli:
        input_pauli_string = ''.join(char for char in input_pauli.to_label() if char.isalpha()) # converts the Pauli to a string w/o phase
        input_pauli_string = input_pauli_string[::-1] # reverses the string so that the first qubit is the first character in the string
    
    nontriv_indices = [index for index, char in enumerate(input_pauli_string) if char != 'I'] # finds the indices of the nontrivial Pauli gates

    prep_circ = qk.QuantumCircuit(len(input_pauli_string))
    p_eigenstate = [random.choice(range(2)) for i in nontriv_indices] # randomly chooses |psi+> (0) or |psi-> (1)
    
    for index, qubit in enumerate(nontriv_indices):
        pauli_gate = input_pauli_string[qubit]
        if pauli_gate == "X": # if the input Pauli is X
            if p_eigenstate[index] == 0: # if the randomly chosen eigenvector is |+>
                prep_circ.h(qubit)
            elif p_eigenstate[index] == 1: # if the randomly chosen eigenvector is |->
                prep_circ.x(qubit)
                prep_circ.h(qubit)
        elif pauli_gate == "Y": # if the input Pauli is Y
            if p_eigenstate[index] == 0: # if the randomly chosen eigenvector is l+i>
                prep_circ.h(qubit)
                prep_circ.s(qubit)
            elif p_eigenstate[index] == 1: # if the randomly chosen eigenvector is |-i>
                prep_circ.x(qubit)
                prep_circ.h(qubit)
                prep_circ.s(qubit)
        elif pauli_gate == "Z": # if the input Pauli is Z
            # we don't need to append anything if the chosen eigenstate is 10>, since the input will already be in that state
            if p_eigenstate[index] == 1: # if the randomly chosen eigenvector is
                prep_circ.x(qubit)

    p_in_eigenstate = sum(p_eigenstate) % 2
    return prep_circ, p_in_eigenstate

def measure_circuit(final_pauli):
    if type(final_pauli) == str:
        final_pauli_string = ''.join(char for char in final_pauli if char.isalpha()) # removes the phase from the Pauli string if present
    elif type(final_pauli) == qk.quantum_info.Pauli:
        final_pauli_string = ''.join(char for char in final_pauli.to_label() if char.isalpha()) # converts the Pauli to a string w/o phase
        final_pauli_string = final_pauli_string[::-1] # reverses the string so that the first qubit is the first character in the string

    nontriv_indices = [index for index, char in enumerate(final_pauli_string) if char != 'I'] # finds the indices of the nontrivial Pauli gates
    nontriv_gates = [final_pauli_string[index] for index in nontriv_indices]

    measurement_circ = qk.QuantumCircuit(len(final_pauli_string),len(nontriv_indices))
    # On the measurement circ, we need to dagger the transforms used to prepare the prep circ to measure in the bases given by P'
    for index, g in enumerate(nontriv_gates):
        # print(index)
        if g == "X":
            measurement_circ.h(nontriv_indices[index]) # rotate into X basis
            measurement_circ.measure(nontriv_indices[index],index) # then measure
        elif g == "Y":
            measurement_circ.sdg(nontriv_indices[index])
            measurement_circ.h(nontriv_indices[index]) # S**-1 H rotates into Y basis
            measurement_circ.measure(nontriv_indices[index],index) # then measure
        elif g == "Z":
            measurement_circ.measure(nontriv_indices[index],index) # measure

    return measurement_circ

def est_Lambda(input_pauli,circuit_ensemble,num_experiments):

    if type(input_pauli) == str:
        input_pauli_string = ''.join(char for char in input_pauli if char.isalpha()) # removes the phase from the Pauli string if present
    elif type(input_pauli) == qk.quantum_info.Pauli:
        input_pauli_string = ''.join(char for char in input_pauli.to_label() if char.isalpha()) # converts the Pauli to a string w/o phase
        input_pauli_string = input_pauli_string[::-1] # reverses the string so that the first qubit is the first character in the string

    freq_dict = random_choices_with_counts([circ.name for circ in circuit_ensemble],num_experiments)

    eigenresults_dict = {("+","+"):0,("+","-"):0,("-","+"):0,("-","-"):0}
    for circ_name in freq_dict:
        circ = find_circuit_from_name(circuit_ensemble,circ_name)
        num_shots = freq_dict[circ_name]
        start_in_plus = random.randint(1, num_shots)
        starter = [start_in_plus, num_shots - start_in_plus]
        
        p_in_eigenstate = 100
        for i in [0,1]:
            while p_in_eigenstate != i:
                prep_circ,p_in_eigenstate = prep_circuit(input_pauli_string)
        
            if p_in_eigenstate == 0:
                p_eigenstate = "+"
            elif p_in_eigenstate == 1:
                p_eigenstate = "-"
            
            prep_circ.barrier()

            measure_circ = measure_circuit(Clifford_Permute(circ,input_pauli_string))

            temp_circuit = prep_circ.compose(circ)
            temp_circuit.barrier()
            full_circuit = temp_circuit.compose(measure_circ)
            # print(full_circuit)
        
            # Simulate the circuit with the stabilizer simulator
            simulator = Aer.get_backend('aer_simulator', method='stabilizer')
            result = qk.execute(full_circuit, backend = simulator, shots = starter[i]).result()
            counts = result.get_counts()

            for r in counts:
                parity = sum(int(x) for x in r if x.isdigit()) % 2
                if parity == 0:
                    pp_eigenstate = "+"
                elif parity == 1:
                    pp_eigenstate= "-"

                if (p_eigenstate,pp_eigenstate) not in eigenresults_dict:
                    eigenresults_dict[(p_eigenstate,pp_eigenstate)] = counts[r]
                else:
                    eigenresults_dict[(p_eigenstate,pp_eigenstate)] += counts[r]

    # print(sum(eigenresults_dict.values()))
    # Lambda_est = ((eigenresults_dict[("+","+")] - eigenresults_dict[("+","-")])/(eigenresults_dict[("+","+")] + eigenresults_dict[("+","-")]) - (eigenresults_dict[("-","+")] - eigenresults_dict[("-","-")])/(eigenresults_dict[("-","+")] + eigenresults_dict[("-","-")]))
    Lambda_est = ((eigenresults_dict[("+","+")] - eigenresults_dict[("+","-")]) - (eigenresults_dict[("-","+")] - eigenresults_dict[("-","-")]))/sum(eigenresults_dict.values())

    return Lambda_est

def G_twirling_noisy(circuit):
    '''This function performs G-twirling on a circuit. It randomly chooses a Pauli from {X,Y,Z,I} and prepends it before a layer, then appends P'=CPC^T after the layer.}
    Inputs: circuit - A Qiskit Circuit object.
    Outputs: new_circuit - A Qiskit Circuit object.'''
    num_qubits = circuit.num_qubits
    new_circuit = qk.QuantumCircuit(num_qubits)
    subcirc_list = list(split_circuit_by_barrier(circuit))
    for index, subcircuit in enumerate(split_circuit_by_barrier(circuit)):
        # if len(subcircuit.data) == 1:
        #     operated_qubits = [subcircuit.find_bit(q).index for q in subcircuit.data[0].qubits]
        # else:
        #     operated_qubits = list(range(num_qubits))
        if index % 2 == 0: #if in odd layer
            pauli_str = ''.join(random.choice(["X","Y","Z","I"]) for _ in range(num_qubits))
            pauli = qk.quantum_info.Pauli(pauli_str[::-1])
            new_circuit = new_circuit.compose(pauli,qubits=range(num_qubits))
            new_circuit = new_circuit.compose(subcircuit,qubits=range(num_qubits))
        if index % 2 != 0: #if in even layer
            new_circuit = new_circuit.compose(subcircuit,qubits=range(num_qubits))
            new_circuit = new_circuit.compose(Clifford_Permute(subcirc_list[index-1],pauli_str).to_instruction(),qubits = range(num_qubits))
            if index != len(list(split_circuit_by_barrier(circuit)))-1:
                new_circuit.barrier()
    return new_circuit

# generate A matrix
A = generate_A(width=width, depth=depth)

# generate theta vector
random_theta = (np.random.randint(10, size=A.shape[0]) + 1)/10
random_theta = np.ones(A.shape[0])

# return error vector
lambda_vector = Amatrixsolve(A, random_theta)
error_vector = error(lambda_vector)

print("ERROR VECTOR: ", error_vector)