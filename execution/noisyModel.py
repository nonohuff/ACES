from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit.tools.visualization import plot_histogram
# Import from Qiskit Aer noise module
from qiskit_aer.noise import (NoiseModel, QuantumError, ReadoutError,
    pauli_error, depolarizing_error, thermal_relaxation_error)
from numpy import random

def noisySimulator(cir, px=0, py=0, pz=0, singleGateErrorInstruction=None, doubleGateErrorInstruction=None, shots=1024):

    if singleGateErrorInstruction is None:
        singleGateErrorInstruction = ["u1", "u2", "u3"]

    if doubleGateErrorInstruction is None:
        doubleGateErrorInstruction = ["cx"]

    # px: probability of getting an additional X gate
    # py: probability of getting an additional Y gate
    # pz: probability of getting an additional Z gate
    # 1 - px - py - pz: probability of getting an additional I gate
    singleGateError = pauli_error([('X', px), ('Y', py), ('Z', pz), ('I', 1 - px - py - pz)])
    doubleGateError = singleGateError.tensor(singleGateError)

    # Create a noise model
    noisySim = NoiseModel()
    noisySim.add_all_qubit_quantum_error(singleGateError, singleGateErrorInstruction)
    noisySim.add_all_qubit_quantum_error(doubleGateError, doubleGateErrorInstruction)

    # Initialize Aer simulator backend
    noisySimAer = AerSimulator(noise_model=noisySim)

    # Transpile circuit for noisy basis gates
    cirTranspile = transpile(cir, noisySimAer)

    # Run and get counts
    result = noisySimAer.run(cirTranspile, shots=shots).result()
    return result












