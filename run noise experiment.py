"""
Compares noiseless vs noisy VQE for BOTH the shallow and expressive
ansatzes, under a real-hardware noise model (FakeManilaV2 snapshot).
Run after run_experiment.py.

Requires: qiskit-aer, qiskit-ibm-runtime
    pip install qiskit-aer qiskit-ibm-runtime

Note: the expressive ansatz run takes noticeably longer than shallow
(more parameters -> more parameter-shift circuit evaluations per
iteration). Expect several minutes total for both noisy runs.
"""
import numpy as np
import matplotlib.pyplot as plt

from src.vqe_tfim.hamiltonian import build_hamiltonian
from src.vqe_tfim.ansatz import shallow_ansatz, expressive_ansatz
from src.vqe_tfim.optimizer import run_vqe
from src.vqe_tfim.exact_solver import exact_ground_state
from src.vqe_tfim.noise import run_noisy_vqe

H = build_hamiltonian(J=1, h=0.5)
exact_energy = exact_ground_state(H)

# ── Noiseless baselines (reuse the same settings as run_experiment.py) ────
print("Running noiseless shallow VQE (300 iterations)...")
_, history_clean_s = run_vqe(H, ansatz_fn=shallow_ansatz, n_params=6)

print("Running noiseless expressive VQE (300 iterations)...")
_, history_clean_e = run_vqe(H, ansatz_fn=expressive_ansatz, n_params=9)

# ── Noisy runs (FakeManilaV2 snapshot, finite-shot estimation) ────────────
print("Running noisy shallow VQE under FakeManilaV2 model (60 iterations)...")
_, history_noisy_s = run_noisy_vqe(
    H, ansatz_fn=shallow_ansatz, n_params=6, iterations=60, shots=512
)

print("Running noisy expressive VQE under FakeManilaV2 model (60 iterations)...")
_, history_noisy_e = run_noisy_vqe(
    H, ansatz_fn=expressive_ansatz, n_params=9, iterations=60, shots=512
)

# ── Summary table ───────────────────────────────────────────────────────
def summarize(name, history):
    final = history[-1]
    gap = abs(final - exact_energy)
    auc_norm = np.trapezoid(history) / len(history)
    print(f"  {name:32s} E = {final:9.4f}   gap = {gap:.4f}   AUC(norm) = {auc_norm:.4f}")
    return final, gap, auc_norm

print()
print(f"  Exact energy: {exact_energy:.4f}")
print()
summarize("Shallow, noiseless", history_clean_s)
summarize("Expressive, noiseless", history_clean_e)
_, gap_noisy_s, _ = summarize("Shallow, noisy", history_noisy_s)
_, gap_noisy_e, _ = summarize("Expressive, noisy", history_noisy_e)

print()
print(f"  Expressive/shallow noise-gap ratio: {gap_noisy_e / gap_noisy_s:.2f}x")

# ── Combined plot: shallow vs expressive, under noise ──────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(history_noisy_s, color='steelblue', linewidth=2,
        label='Shallow (noisy, 6 params)')
ax.plot(history_noisy_e, color='darkorange', linewidth=2,
        label='Expressive (noisy, 9 params)')
ax.axhline(exact_energy, color='black', linestyle='--', linewidth=1.5, label='Exact')
ax.set_xlabel('Iteration')
ax.set_ylabel('Energy')
ax.set_title('Noisy VQE Convergence — Shallow vs Expressive Ansatz\n'
             'FakeManilaV2 noise model, 512 shots', fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('noise_comparison_both.png', dpi=150, bbox_inches='tight')
print('\n  Saved: noise_comparison_both.png')