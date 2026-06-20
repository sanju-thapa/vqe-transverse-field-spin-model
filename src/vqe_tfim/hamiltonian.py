from qiskit.quantum_info import SparsePauliOp


def build_hamiltonian(J: float = 1.0, h: float = 0.5) -> SparsePauliOp:
    """
    Three-qubit transverse field Ising model:
    H = J(Z0Z1 + Z1Z2) + h(X0 + X1 + X2)
    """
    return SparsePauliOp(
        ["IZZ", "ZZI", "IIX", "IXI", "XII"],
        coeffs=[J, J, h, h, h],
    )