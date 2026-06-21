from qiskit import QuantumCircuit


def shallow_ansatz(theta) -> QuantumCircuit:
    """
    Shallow ansatz (6 parameters):
    H^3 -> RY(t0,t1,t2) -> CNOT(0,1) -> CNOT(1,2) -> RY(t3,t4,t5)
    """
    qc = QuantumCircuit(3)

    qc.h(0)
    qc.h(1)
    qc.h(2)

    qc.ry(theta[0], 0)
    qc.ry(theta[1], 1)
    qc.ry(theta[2], 2)

    qc.cx(0, 1)
    qc.cx(1, 2)

    qc.ry(theta[3], 0)
    qc.ry(theta[4], 1)
    qc.ry(theta[5], 2)

    return qc