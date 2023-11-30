from generator import generateCliffordCircuit
from calculator import addTwirlingGates
from execution.transpiler import transpileListToQiskitCircuit

width = 4 # num_qubits
depth = 3 # number of layers in the circuit (easy + hard)
singleGateSet = ['X', 'H', 'Z', 'I', 'S']
doubleGateSet = ['CNOT_C', 'CNOT_T']
twirlingGateSet = ['X','Y' 'Z', 'I']

# Generate Clifford circuit
circuit = generateCliffordCircuit(width, depth, singleGateSet, doubleGateSet)
# # Twirl the circuit with Clifford operations
# circuitTwirl = addTwirlingGates(circuit, twirlingGateSet)
# # Fix up the Clifford dagger operator to make the unitaries unchanged.
qiskitCircuit = transpileListToQiskitCircuit(circuit)
print(circuit)
print(qiskitCircuit)
for op in qiskitCircuit.data:
    print(op.operation.name)

