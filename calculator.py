from numpy import random


def addTwirlingGates(cir, twirlingGateSet):
    depth = len(cir)
    width = len(cir[0])
    twirlCir = [[] for _ in range(depth * 3)]
    for i in range(depth):
        iClif = 3 * i
        twirlCir[iClif] = [random.choice(twirlingGateSet) for _ in range(width)]
        iTwirl = 1 + 3 * i
        twirlCir[iTwirl] = cir[i]
    return twirlCir







# for d in range(depth + 1):



