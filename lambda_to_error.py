import numpy as np 
import symplecticform as symplecticform
from generate_A import params_list, singleGateSet, doubleGateSet

def returnindex(cliff, pauli, reference=params_list(singleGateSet+doubleGateSet)):
    'This function goes from the dictionary key to the corresponding index in  the vector format'
    'i.e the dictionary keys look like reference = {("X", "X"), ("X", "Y"), ("X", "Z")...'
    'Hence returnindex("X","Y") = 1'
    #In the defintion above I replace ' by " as ' are a reserved keyword in function definition#
    params = list(reference.keys())
    return params.index((cliff,pauli))

def error(lambda_list, reference = params_list(singleGateSet+doubleGateSet), double_gate_set_pauli = [i[1] for i in list(params_list(doubleGateSet))]):
    'lambda is solution by exponetiating(-solution) to A matrix'
    'lambda will be a 1D array of length given by the reference term'
    'The indices i will sum over all the cliffords and possible pauli errors, exac'
    probvec = np.zeros(len(reference))
    params = list(reference.keys())
    counter = 0
    for i in params:
        counter += 1
        if (i[0] != 'CNOT'):
            sum = 0
            for j in ('X','Y','Z'):
                # sum += symplecticform.sympleticform(i[1],j)*lambda_list[returnindex(i[0],j)]
                sum += symplecticform.sympleticform(i[1],j)*lambda_list[counter-1]
            probvec[returnindex(i[0], i[1])] = sum
        else:
            sum = 0  
            firstpauli = (i[1])[0]
            secondpauli = (i[1])[1]  
            for j in double_gate_set_pauli:
                firstpauli_dum = list(j)[0]
                secondpauli_dum = list(j)[1]
                sum += symplecticform.sympleticform(firstpauli,firstpauli_dum)*symplecticform.sympleticform(secondpauli,secondpauli_dum)*lambda_list[counter-1]
            probvec[returnindex(i[0], i[1])] = sum  
    # return probvec*(1/np.sum(probvec)) #return normalized probability vector
    return probvec #return unnormalized probability vector