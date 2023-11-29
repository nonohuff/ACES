'''
    This file transpiles a quantum circut from list to Qiskit circuit.
'''
from qiskit.circuit import QuantumCircuit
cir = [['X', 'H'], ['CNOT_C', 'CNOT_T'], ['Z', 'I']]

def transpileListToQiskitCircuit(cir):
    depth = len(cir)
    width = len(cir[0])
    qiskitCir = QuantumCircuit(width)
    for d in range(width):
        if d % 2 == 0:
            for w in range(width):
                singleGate = cir[d][w]
                stringToQiskitSingleGate(singleGate, qiskitCir, w)
            qiskitCir.barrier()
        else:
            c = cir[d].index('CNOT_C')
            t = cir[d].index('CNOT_T')
            qiskitCir.cx(c, t)
            qiskitCir.barrier()
    return qiskitCir

def stringToQiskitSingleGate(gateString, qiskitCir, whichQubit):
    if gateString == 'I':
        qiskitCir.i(whichQubit)
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
