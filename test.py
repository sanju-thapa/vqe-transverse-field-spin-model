from src.vqe_tfim.hamiltonian import build_hamiltonian

H = build_hamiltonian(J=1, h=0.5)
print(H)