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

def fixTwirlingDagger(cirTwirl):
    depth = len(cirTwirl)
    width = len(cirTwirl[0])
    idx = int(depth / 3)
    for i in range(idx):
        daggerIdx = 2 + 3 * i
        for w in range(width):
            cirTwirl[daggerIdx][w] =
    cirTwirl

def stabilize(p1, p2):
    if p1 == 'I':
        return p1
    elif p1 == 'X':
        return p1






# for d in range(depth + 1):



