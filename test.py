from src.vqe_tfim.hamiltonian import build_hamiltonian
from src.vqe_tfim.optimizer import run_vqe
from src.vqe_tfim.exact_solver import exact_ground_state

H = build_hamiltonian(J=1, h=0.5)
theta_final, history = run_vqe(H)
exact_energy = exact_ground_state(H)

print("VQE final energy:   ", history[-1])
print("Exact ground energy:", exact_energy)
print("Difference:         ", abs(history[-1] - exact_energy))
print("Last 10 energy values:", history[-10:])