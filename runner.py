# imports
from generate_A import generate_A
from amatrixsolver import Amatrixsolve
from lambda_to_error import error
import numpy as np

# variables
width = 5
depth = 5

# generate A matrix
A = generate_A(width=width, depth=depth)

# generate theta vector
random_theta = (np.random.randint(10, size=A.shape[0]) + 1)/10
random_theta = np.ones(A.shape[0])

# return error vector
lambda_vector = Amatrixsolve(A, random_theta)
error_vector = error(lambda_vector)

print("ERROR VECTOR: ", error_vector)