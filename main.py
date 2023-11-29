from generator import generateCliffordCircuit
from calculator import addTwirlingGates
from execution.transpiler import transpileListToQiskitCircuit

width = 3
depth = 3
singleGateSet = ['X', 'H', 'Z', 'I']
doubleGateSet = ['CNOT_C', 'CNOT_T']
twirlingGateSet = ['X', 'Z', 'I']

# Generate Clifford circuit
circuit = generateCliffordCircuit(width, depth, singleGateSet, doubleGateSet)
# # Twirl the circuit with Clifford operations
# circuitTwirl = addTwirlingGates(circuit, twirlingGateSet)
# # Fix up the Clifford dagger operator to make the unitaries unchanged.
qiskitCircuit = transpileListToQiskitCircuit(circuit)
print(circuit)
print(qiskitCircuit)


