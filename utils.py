from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit.tools.visualization import plot_histogram
# Import from Qiskit Aer noise module
from qiskit_aer.noise import (NoiseModel, QuantumError, ReadoutError,
                              pauli_error, depolarizing_error, thermal_relaxation_error)
from numpy import random
from qiskit.circuit.library import XGate, YGate, ZGate, HGate, SGate, TGate, CXGate, IGate


def IMatrix(): return IGate().to_matrix()


def XMatrix(): return XGate().to_matrix()


def YMatrix(): return YGate().to_matrix()


def ZMatrix(): return ZGate().to_matrix()


def HMatrix(): return HGate().to_matrix()


def SMatrix(): return SGate().to_matrix()


def TMatrix(): return TGate().to_matrix()


results =
def plotResults(results):


# def CXMatrix(): return CXGate().to_matrix()


