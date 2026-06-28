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

def expressive_ansatz(theta) -> QuantumCircuit:
    '''
    Expressive ansatz (9 parameters):
    H^3 -> RY(t0,t1,t2) -> CNOT(0,1) -> RY(t3,t4,t5) -> COT(1,2) ->RY(t6,t7,t8)
    '''
    qc = QuantumCircuit(3)
    # 1. Hadamard on all 3 qubits
    qc.h([0, 1, 2])

    # 2. First RY layer
    qc.ry(theta[0], 0)
    qc.ry(theta[1], 1)
    qc.ry(theta[2], 2)

    # 3. First entangling layer
    qc.cx(0, 1)
    qc.cx(1, 2)

    # 4. Second RY layer
    qc.ry(theta[3], 0)
    qc.ry(theta[4], 1)
    qc.ry(theta[5], 2)

    # 5. Second entangling layer
    qc.cx(0, 1)
    qc.cx(1, 2)

    # 6. Third RY layer
    qc.ry(theta[6], 0)
    qc.ry(theta[7], 1)
    qc.ry(theta[8], 2)

    return qc