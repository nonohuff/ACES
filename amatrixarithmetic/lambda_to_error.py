import numpy as np 
import symplecticform

def returnindex(cliff, pauli, reference=params_list(singleGateSet+doubleGateSet)):
    'This function goes from the dictionary key to the corresponding index in  the vector format'
    'i.e the dictionary keys look like reference = {("X", "X"), ("X", "Y"), ("X", "Z")...'
    'Hence returnindex("X","Y") = 1'
    #In the defintion above I replace ' by " as ' are a reserved keyword in function definition#
    params = list(reference.keys())
    return params.index((cliff,pauli))

def error(lambda_, reference = params_list(singleGateSet+doubleGateSet), double_gate_set_pauli = [i[1] for i in list(params_list(doubleGateSet))]):
    'lambda is solution by exponetiating(-solution) to A matrix'
    'lambda will be a 1D array of length given by the reference term'
    'The indices i will sum over all the cliffords and possible pauli errors, exac'
    probvec = np.array([])
    params = list(reference.keys())
    for i in params:
        if (i[0] != 'CNOT'):
            sum = 0
            for j in ('X','Y','Z','I'):
                sum += (0.5)*symplecticform(i[1],j)*lambda_[returnindex(i[0],j)]
            probvec[returnindex(i)] = sum
        else:
            sum = 0  
            firstpauli = list(i)[0]
            secondpauli = list(i)[1]  
            for j in double_gate_set_pauli:
                firstpauli_dum = list(j)[0]
                secondpauli_dum = list(j)[1]
                sum += (0.25)*symplecticform(firstpauli,firstpauli_dum)*symplecticform(secondpauli,secondpauli_dum)*lambda_[returnindex('CNOT',j)]
            probvec[returnindex(i)] = sum    
    return probvec 