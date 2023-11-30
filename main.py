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

# Measure all qubits
# qiskitCircuit.measure_all()
# qiskitCircuitTwirl.measure_all()


# Simulate the circuit using noisy Aer backend


# Define the instructions for Pauli error
# Instructions to apply the single qubit Pauli gate error
# singleGateErrorInstruction = ['noisyI', 'noisyX', 'noisyY', 'noisyZ', 'noisyH', 'noisyS']
singleGateErrorInstruction = ['u1', 'u2', 'u3']
# Instructions to apply the double qubit gate error, i.e. tensor of two single qubit Pauli gate error
# doubleGateErrorInstruction = ['noisyCX']
doubleGateErrorInstruction = ['noisyCX']




# # Run the circuit with noisy backend
# result = noisySimulator(qiskitCircuitTwirl, px=px, py=py, pz=pz,
#                         singleGateErrorInstruction=singleGateErrorInstruction,
#                         doubleGateErrorInstruction=doubleGateErrorInstruction, shots=shots)
# print(result.get_counts(0))
# # Run the circuit with noisy backend
# result = noisySimulator(qiskitCircuit, px=px, py=py, pz=pz,
#                         singleGateErrorInstruction=singleGateErrorInstruction,
#                         doubleGateErrorInstruction=doubleGateErrorInstruction, shots=shots)
# print(result.get_counts(0))






