import numpy as np

def Amatrixsolve(Amatrix,Lambda):
    'Amatrix: numpy 2D array'
    'Lmabda: numpy 1D array'

    Lambda = np.abs(Lambda)

    if (np.linalg.matrix_rank(Amatrix) != Amatrix.shape[0]):
        raise ValueError('Amatrix is not of full rank')
    if (0 in Lambda):
        raise ValueError('The log of Lambda matrix cannot be taken as zero element somewhere in vector')
    b = -np.log(Lambda) 
    if Amatrix.shape[0] == Amatrix.shape[1]: #Checking whether matrix is square or not if not square use least squares#
        x = np.linalg.solve(Amatrix,b)
        return np.exp(-x) #return negative exponentiation of solution for small lambda
    else: #If matrix is non square, resort to least squares to find solution
        x = np.linalg.lstsq(Amatrix,b)
        if (len(x) != 0): #If multiple solutions exist for least squares choose first solution arbitrarily
            x = x[0]
            return np.exp(-x) #return negative exponentiation of solution for small lambda
        else:
            return np.exp(-x) #return negative exponentiation of solution for small lambda