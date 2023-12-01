from generator import generateCliffordCircuit
from execution.transpiler import transpileListToQiskitCircuit
from twirler import GTwirling

width = 4  # num_qubits
depth = 3  # number of layers in the circuit (easy + hard)
singleGateSet = ['X', 'H', 'Z', 'I', 'S']
# singleGateSet = ['X']

doubleGateSet = ['CNOT_C', 'CNOT_T']
twirlingGateSet = ['X', 'Y' 'Z', 'I']

shots = 100000
# Define a Pauli error channel
px = 0.05  # adjust the probability as needed
py = 0.10  # adjust the probability as needed
pz = 0.20  # adjust the probability as needed

# Generate Clifford circuit
circuit = generateCliffordCircuit(width, depth, singleGateSet, doubleGateSet)
# # Twirl the circuit with Clifford operations
# circuitTwirl = addTwirlingGates(circuit, twirlingGateSet)
# # Fix up the Clifford dagger operator to make the unitaries unchanged.
qiskitCircuit =transpileListToQiskitCircuit(circuit)
print(qiskitCircuit)
qiskitCircuitNoisy = transpileListToQiskitCircuit(circuit, noise=True, px=px, py=py, pz=pz)
# print(circuit)
print(qiskitCircuitNoisy)
# for op in qiskitCircuit.data:
#     print(op.operation.name)
qiskitCircuitTwirl = GTwirling(qiskitCircuit)
print(qiskitCircuitTwirl)



