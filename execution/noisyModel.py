from numpy import random
from qiskit_aer import AerSimulator
from qiskit import transpile


def makeNoisyGates(qiskitCir, whichQubits, px=0, py=0, pz=0):
    singleOrDouble = len(whichQubits)
    if singleOrDouble == 1:
        gateString = random.choice(['I', 'X', 'Y', 'Z'], p=[1-px-py-pz, px, py, pz])
        if gateString == 'I':
            qiskitCir.i(whichQubits[0])
        elif gateString == 'X':
            qiskitCir.x(whichQubits[0])
        elif gateString == 'Y':
            qiskitCir.y(whichQubits[0])
        elif gateString == 'Z':
            qiskitCir.z(whichQubits[0])
    else:
        gateString1 = random.choice(['I', 'X', 'Y', 'Z'], p=[1-px-py-pz, px, py, pz])
        if gateString1 == 'I':
            qiskitCir.i(whichQubits[0])
        elif gateString1 == 'X':
            qiskitCir.x(whichQubits[0])
        elif gateString1 == 'Y':
            qiskitCir.y(whichQubits[0])
        elif gateString1 == 'Z':
            qiskitCir.z(whichQubits[0])
        gateString2 = random.choice(['I', 'X', 'Y', 'Z'], p=[1-px-py-pz, px, py, pz])
        if gateString2 == 'I':
            qiskitCir.i(whichQubits[1])
        elif gateString2 == 'X':
            qiskitCir.x(whichQubits[1])
        elif gateString2 == 'Y':
            qiskitCir.y(whichQubits[1])
        elif gateString2 == 'Z':
            qiskitCir.z(whichQubits[1])
    return qiskitCir


def simulateAer(qiskitCir, shots=1024):
# Initialize Aer simulator backend
    AerSim = AerSimulator()
    qiskitCirTranspile = transpile(qiskitCir, AerSim)
    result = AerSim.run(qiskitCirTranspile, shots=shots).result()
    return result







# def noisySimulator(cir, px=0, py=0, pz=0, singleGateErrorInstruction=None, doubleGateErrorInstruction=None, shots=1024):
#     if singleGateErrorInstruction is None:
#         singleGateErrorInstruction = ["u1", "u2", "u3"]
#
#     if doubleGateErrorInstruction is None:
#         doubleGateErrorInstruction = ["cx"]
#
#     # px: probability of getting an additional X gate
#     # py: probability of getting an additional Y gate
#     # pz: probability of getting an additional Z gate
#     # 1 - px - py - pz: probability of getting an additional I gate
#     singleGateError = pauli_error([('X', px), ('Y', py), ('Z', pz), ('I', 1 - px - py - pz)])
#     doubleGateError = singleGateError.tensor(singleGateError)
#
#     # Create a noise model
#     noisySim = NoiseModel()
#     noisySim.add_basis_gates('unitary')
#     noisySim.add_all_qubit_quantum_error(singleGateError, singleGateErrorInstruction)
#     noisySim.add_all_qubit_quantum_error(doubleGateError, doubleGateErrorInstruction)
#
#     # Initialize Aer simulator backend
#     noisySimAer = AerSimulator(noise_model=noisySim)
#
#     # Transpile circuit for noisy basis gates
#     cirTranspile = transpile(cir, noisySimAer)
#
#     # Run and get counts
#     result = noisySimAer.run(cirTranspile, shots=shots).result()
#     return result
