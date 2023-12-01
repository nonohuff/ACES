from generator import generateCliffordCircuit
from twirler import GTwirling
from numpy import random
from qiskit.circuit import QuantumCircuit

# Necessary functions
def makeNoisyGates(qiskitCir, whichQubits, px=0, py=0, pz=0):
    singleOrDouble = len(whichQubits)
    if singleOrDouble == 1:
        gateString = random.choice(['I', 'X', 'Y', 'Z'], p=[1-px-py-pz, px, py, pz])
        if gateString == 'I':
            qiskitCir.id(whichQubits[0])
        elif gateString == 'X':
            qiskitCir.x(whichQubits[0])
        elif gateString == 'Y':
            qiskitCir.y(whichQubits[0])
        elif gateString == 'Z':
            qiskitCir.z(whichQubits[0])
    else:
        gateString1 = random.choice(['I', 'X', 'Y', 'Z'], p=[1-px-py-pz, px, py, pz])
        if gateString1 == 'I':
            qiskitCir.id(whichQubits[0])
        elif gateString1 == 'X':
            qiskitCir.x(whichQubits[0])
        elif gateString1 == 'Y':
            qiskitCir.y(whichQubits[0])
        elif gateString1 == 'Z':
            qiskitCir.z(whichQubits[0])
        gateString2 = random.choice(['I', 'X', 'Y', 'Z'], p=[1-px-py-pz, px, py, pz])
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


width = 4  # num_qubits
depth = 3  # number of layers in the circuit (easy + hard)
singleGateSet = ['X', 'H', 'Z', 'I', 'S']
doubleGateSet = ['CNOT_C', 'CNOT_T']
twirlingGateSet = ['X', 'Y' 'Z', 'I']

shots = 100000
# Define a Pauli error channel
px = 0.05  # adjust the probability as needed
py = 0.10  # adjust the probability as needed
pz = 0.20  # adjust the probability as needed

# Generate Clifford circuit and transpile to ideal qiskit circuit
circuit = generateCliffordCircuit(width, depth, singleGateSet, doubleGateSet)
qiskitCircuit =transpileListToQiskitCircuit(circuit)
print(qiskitCircuit)
# Generate Clifford circuit and transpile to noisy qiskit circuit
qiskitCircuitNoisy = transpileListToQiskitCircuit(circuit, noise=True, px=px, py=py, pz=pz)
print(qiskitCircuitNoisy)
# Twirling function
qiskitCircuitTwirl = GTwirling(qiskitCircuit)
print(qiskitCircuitTwirl)

from qiskit_aer import AerSimulator
from qiskit import transpile
def simulateAer(qiskitCir, shots=1024):
    qiskitCir.measure_all()
    # Initialize Aer simulator backend
    AerSim = AerSimulator()
    qiskitCirTranspile = transpile(qiskitCir, AerSim)
    result = AerSim.run(qiskitCirTranspile, shots=shots).result()
    return result

result = simulateAer(qiskitCircuitTwirl, shots=shots)
counts = result.get_counts()
print(result)
print(counts)

