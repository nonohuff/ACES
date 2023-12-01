from qiskit import QuantumCircuit, quantum_info
from numpy import random

def CliffordPermute(cliff, pauli):
    '''This function permutes the pauli operators according to the clifford group, so it computes
    P' = C P C^T, where C is a clifford operator and P is a pauli operator.
    Inputs: cliff - A Qiskit Circuit, Clifford, or Gate object.
            pauli - A Qiskit Pauli object.
    Outputs: new_pauli - A Qiskit Pauli object.'''

    return pauli.evolve(cliff,frame="s")

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
        yield QuantumCircuit.from_qasm_str('\n'.join(circuit_with_prelude))


def GTwirling(circuit):
    '''This function performs G-twirling on a circuit. It randomly chooses a Pauli from {X,Y,Z,I} and prepends it before a layer, then appends P'=CPC^T after the layer.}
    Inputs: circuit - A Qiskit Circuit object.
    Outputs: new_circuit - A Qiskit Circuit object.'''
    num_qubits = circuit.num_qubits
    new_circuit = QuantumCircuit(num_qubits)
    for index, subcircuit in enumerate(split_circuit_by_barrier(circuit)):
        # if len(subcircuit.data) == 1:
        #     operated_qubits = [subcircuit.find_bit(q).index for q in subcircuit.data[0].qubits]
        # else:
        #     operated_qubits = list(range(num_qubits))
        pauli_str = ''.join(random.choice(["X","Y","Z","I"]) for _ in range(num_qubits))
        pauli = quantum_info.Pauli(pauli_str)
        new_circuit = new_circuit.compose(pauli,qubits=range(num_qubits))
        new_circuit = new_circuit.compose(subcircuit,qubits=range(num_qubits))
        new_circuit = new_circuit.compose(CliffordPermute(subcircuit,pauli).to_instruction(),qubits = range(num_qubits))
        if index != len(list(split_circuit_by_barrier(circuit)))-1:
            new_circuit.barrier()
    return new_circuit