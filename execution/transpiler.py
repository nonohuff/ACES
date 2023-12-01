'''
    This file transpiles a quantum circut from list to Qiskit circuit.
'''
from qiskit.circuit import QuantumCircuit
from utils import IMatrix, XMatrix, YMatrix, ZMatrix, HMatrix, SMatrix
from execution.noisyModel import makeNoisyGates

cir = [['X', 'H'], ['CNOT_C', 'CNOT_T'], ['Z', 'I']]

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

# def stringToQiskitSingleGate(gateString, qiskitCir, whichQubit):
#     if gateString == 'I':
#         qiskitCir.i(whichQubit, label='noisyI')
#     elif gateString == 'X':
#         qiskitCir.x(whichQubit, label='noisyX')
#     elif gateString == 'Y':
#         qiskitCir.y(whichQubit, label='noisyY')
#     elif gateString == 'Z':
#         qiskitCir.z(whichQubit, label='noisyZ')
#     elif gateString == 'H':
#         qiskitCir.h(whichQubit, label='noisyH')
#     elif gateString == 'S':
#         qiskitCir.s(whichQubit, label='noisyS')

# def stringToQiskitSingleGate(gateString, qiskitCir, whichQubit):
#     if gateString == 'I':
#         qiskitCir.unitary(IMatrix(), [whichQubit], label='noisyI')
#     elif gateString == 'X':
#         qiskitCir.unitary(XMatrix(), [whichQubit], label='noisyX')
#     elif gateString == 'Y':
#         qiskitCir.unitary(YMatrix(), [whichQubit], label='noisyY')
#     elif gateString == 'Z':
#         qiskitCir.unitary(ZMatrix(), [whichQubit], label='noisyZ')
#     elif gateString == 'H':
#         qiskitCir.unitary(HMatrix(), [whichQubit], label='noisyH')
#     elif gateString == 'S':
#         qiskitCir.unitary(SMatrix(), [whichQubit], label='noisyS')