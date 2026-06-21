from src.vqe_tfim.hamiltonian import build_hamiltonian
from src.vqe_tfim.ansatz import shallow_ansatz

H = build_hamiltonian(J=1, h=0.5)
print(H)

theta = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
qc = shallow_ansatz(theta)
print(qc)