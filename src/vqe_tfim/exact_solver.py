import numpy as np
from qiskit.quantum_info import SparsePauliOp


def exact_ground_state(hamiltonian: SparsePauliOp) -> float:
    """
    Compute the exact ground state energy by diagonalizing
    the full Hamiltonian matrix directly (no VQE involved).
    """
    matrix = hamiltonian.to_matrix()
    eigenvalues, _ = np.linalg.eigh(matrix)
    return eigenvalues[0]