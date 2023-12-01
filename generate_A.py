# import relevant libraries. 
import numpy as np
import qiskit as qk
from collections import Counter
from collections import OrderedDict

from generator import generateCliffordCircuit
from twirler import split_circuit_by_barrier

# width = 5 # num_qubits
# depth = 5 # number of layers in the circuit (easy + hard)
singleGateSet = ['X', 'H', 'Z', 'S']
doubleGateSet = ['CNOT_C', 'CNOT_T']
# twirlingGateSet = ['X','Y' 'Z', 'I']

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
        
def transpileListToQiskitCircuit(cir):
    depth = len(cir)
    width = len(cir[0])
    qiskitCir = qk.QuantumCircuit(width)
    for d in range(width):
        if d % 2 == 0:
            for w in range(width):
                singleGate = cir[d][w]
                stringToQiskitSingleGate(singleGate, qiskitCir, w)
            if d != width - 1:
                qiskitCir.barrier()
        else:
            c = cir[d].index('CNOT_C')
            t = cir[d].index('CNOT_T')
            qiskitCir.cx(c, t)
            if d != width - 1:
                qiskitCir.barrier()
    return qiskitCir

def Clifford_Permute(cliff,pauli):
    '''This function permutes the pauli operators according to the clifford group, so it computes 
    P' = C P C^T, where C is a clifford operator and P is a pauli operator.
    Inputs: cliff - A Qiskit Circuit, Clifford, or Gate object.
            pauli - A Qiskit Pauli object.
    Outputs: new_pauli - A Qiskit Pauli object.'''

    return pauli.evolve(cliff,frame="s")

def params_list(operation_set, pauli_set=["X","Y","Z","I"]):
    '''This function generates a dictionary of parameters for the given operation set.
    Inputs: operation_set - A list of operations.
            pauli_set - A list of pauli operators.
    Outputs: params - A dictionary of parameters, with each set to 0.'''

    # imporant to use OrderedDict so that the order of the parameters is always the same
    params = OrderedDict()

    for operation in operation_set:
        # don't care about the identity
        if operation == "I":
            continue

        # for CNOT, we need to loop over all pairs of paulis
        elif operation == "CNOT_C" or operation == "CNOT_T" or operation == "CX":
            for pauli1 in pauli_set:
                for pauli2 in pauli_set:
                    # if we have the pauli "II", then skip
                    if pauli1 == "I" and pauli2 == "I":
                        continue
                    pauli = pauli1+pauli2
                    params[("CNOT", pauli)] = 0

        # for single qubit gates, we only need to loop over the paulis, and add the pauli and operation to dict
        else:
            for pauli in pauli_set:
                if pauli == "I":
                    continue
                params[(operation, pauli)] = 0
    return params

def generate_first_layer(length, pauli_set=["X","Y","Z","I"]):
    first_layer = ""
    for ele in np.random.choice(pauli_set, length):
        first_layer += ele
    return first_layer.upper()

def generate_row_A(circuit, input_pauli, params_dict=params_list(singleGateSet+doubleGateSet)):
    '''This function generates a row of the circuit, which is the values of a dictionary of pauli operators and their counts.'''
    # print(random_circuit)

    if type(input_pauli) == str:
        input_pauli_str = ''.join(char for char in input_pauli if char.isalpha()) # removes the phase from the Pauli string if present
    elif type(input_pauli) == qk.quantum_info.Pauli:
        input_pauli_str = ''.join(char for char in input_pauli.to_label() if char.isalpha()) # converts the Pauli to a string w/o phase

    # get from circuit the 1) input pauli string, 2) empty dictionary, and 3) list of all possible operations to check against: 
    pauli_str = input_pauli_str
    curr_row_dict = params_dict.copy()
    all_operations = curr_row_dict.keys()
    i_count = 0
    # iterate each gate in each layer of the circuit 
    for layer in split_circuit_by_barrier(circuit):
        for gate in layer:
            # get the register of the current gate
            register = circuit.find_bit(gate.qubits[0]).index

            # get the gate's operator and the input pauli
            input_gate = gate.operation.name.upper()
            cur_pauli = pauli_str[register]
            
            # store current operation in the dictionary
            if (input_gate, cur_pauli) in all_operations:
                curr_row_dict[(input_gate, cur_pauli)] += 1

            # if its a cnot, there's a different format of the pauli operator
            elif input_gate == 'CX' or input_gate == 'CNOT':
                cur_pauli = pauli_str[layer.data[0][1][0].index] + pauli_str[layer.data[0][1][1].index]

                # don't consider II for the cnot gate
                if cur_pauli == "II":
                    continue 
                curr_row_dict[('CNOT', cur_pauli)] += 1
                continue

            # if it is an identity or barrier gate, skip it
            elif input_gate == 'ID' or input_gate == 'I' or input_gate == 'BARRIER':
                i_count += 1
                continue

        # use predefined function to update the pauli layer
        pauli = Clifford_Permute(layer, qk.quantum_info.Pauli(pauli_str))
        pauli_str = ''.join(char for char in pauli.to_label() if char.isalpha())

    return curr_row_dict.values()

def generate_A(width, depth, params_dict=params_list(singleGateSet+doubleGateSet)):
    '''This function generates the A matrix by randomly generating each row, checking if it increases the rank and then continuing onwards
    Inputs: numrow - The number of rows in the A matrix.
            numcol - The number of columns in the A matrix.
    Outputs: A - The A matrix.'''

    A = []
    counter = 0
    while np.linalg.matrix_rank(A) < len(list(params_dict.keys())):

        # generate the random circuit
        random_circuit = transpileListToQiskitCircuit(generateCliffordCircuit(width, depth, singleGateSet, doubleGateSet))

        # generate input string of type "XYIYX"
        input_pauli_str = generate_first_layer(random_circuit.num_qubits)

        # generate a row of A
        new_row = list(generate_row_A(random_circuit, input_pauli_str, params_dict))

        # check if the row increases the rank of A, then append it to A
        A_star = A.copy()
        A_star.append(new_row)
        if np.linalg.matrix_rank(np.array(A_star)) > np.linalg.matrix_rank(np.array(A)):
            A = A_star
        else:
            # otherwise mark that it didn't work and try again
            counter += 1
        if counter > 100:
            break

    return np.array(A)

# A = generate_A(width = 5, depth = 5)
# print(A)