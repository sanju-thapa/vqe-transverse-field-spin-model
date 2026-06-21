from src.vqe_tfim.hamiltonian import build_hamiltonian
from src.vqe_tfim.optimizer import run_vqe

H = build_hamiltonian(J=1, h=0.5)
theta_final, history = run_vqe(H)

print("Final energy:", history[-1])
print("Number of iterations recorded:", len(history))