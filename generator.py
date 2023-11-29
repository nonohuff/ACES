'''
    Generate the random circuit.
'''
from numpy import random

def generateCliffordCircuit(width, depth, singleGateSet, doubleGateSet):
    # cir = [['X', 'H'], ['CNOT_C', 'CNOT_T'], ['Z', 'I']]
    qubits = list(range(width))
    cir = [['I' for _ in range(width)] for _ in range(depth)]
    for d in range(width):
        if d % 2 == 0:
            for w in range(width):
                randSingleGate = random.choice(singleGateSet)
                cir[d][w] = randSingleGate
        else:
            c, t = doubleGateSet
            randQubits = qubits[:]
            randControl = random.choice(randQubits)
            cir[d][randControl] = c
            randQubits.remove(randControl)
            randTarget = random.choice(randQubits)
            cir[d][randTarget] = t
    return cir










