import numpy as np
import matplotlib.pyplot as plt
from src.vqe_tfim.hamiltonian import build_hamiltonian
from src.vqe_tfim.ansatz import shallow_ansatz, expressive_ansatz
from src.vqe_tfim.optimizer import run_vqe
from src.vqe_tfim.exact_solver import exact_ground_state

# ── Setup ──────────────────────────────────────────────────────────────────
H = build_hamiltonian(J=1, h=0.5)
exact_energy = exact_ground_state(H)

print("=" * 55)
print("  VQE — 3-Qubit Transverse Field Ising Model")
print("=" * 55)
print(f"  Exact ground state energy: {exact_energy:.6f}")
print()

# ── Run VQE (shallow) ──────────────────────────────────────────────────────
theta_shallow, history_shallow = run_vqe(
    H, ansatz_fn=shallow_ansatz, n_params=6
)
vqe_shallow = history_shallow[-1]
gap_shallow = abs(vqe_shallow - exact_energy)

print(f"  Shallow ansatz  →  E = {vqe_shallow:.6f}  |  gap = {gap_shallow:.6f}")

# ── Run VQE (expressive) ───────────────────────────────────────────────────
theta_expressive, history_expressive = run_vqe(
    H, ansatz_fn=expressive_ansatz, n_params=9
)
vqe_expressive = history_expressive[-1]
gap_expressive = abs(vqe_expressive - exact_energy)

print(f"  Expressive ansatz → E = {vqe_expressive:.6f}  |  gap = {gap_expressive:.6f}")
print(f"\n  Gap closed by expressive ansatz: "
      f"{(1 - gap_expressive/gap_shallow)*100:.1f}%")
print("=" * 55)

# ── Plot 1: Energy Convergence Comparison ──────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("VQE Energy Convergence — 3-Qubit TFIM", fontsize=14, fontweight='bold')

axes[0].plot(history_shallow, color='steelblue', linewidth=2)
axes[0].axhline(exact_energy, color='red', linestyle='--', linewidth=1.5, label='Exact')
axes[0].set_title("Shallow Ansatz (6 parameters)")
axes[0].set_xlabel("Iteration")
axes[0].set_ylabel("Energy")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(history_expressive, color='darkorange', linewidth=2)
axes[1].axhline(exact_energy, color='red', linestyle='--', linewidth=1.5, label='Exact')
axes[1].set_title("Expressive Ansatz (9 parameters)")
axes[1].set_xlabel("Iteration")
axes[1].set_ylabel("Energy")
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("convergence_comparison.png", dpi=150, bbox_inches='tight')
print("\n  Saved: convergence_comparison.png")

# ── Plot 2: Expressibility Gap Bar Chart ──────────────────────────────────
fig2, ax = plt.subplots(figsize=(7, 5))
labels = ['Exact\nDiagonalization', 'Expressive\nAnsatz', 'Shallow\nAnsatz']
values = [exact_energy, vqe_expressive, vqe_shallow]
colors = ['#2ecc71', '#e67e22', '#3498db']

bars = ax.bar(labels, values, color=colors, width=0.5, edgecolor='white', linewidth=1.2)
ax.set_ylabel("Ground State Energy")
ax.set_title("Ansatz Expressibility Gap\n3-Qubit TFIM (J=1, h=0.5)", fontweight='bold')
ax.set_ylim([min(values) - 0.1, 0])
ax.grid(True, axis='y', alpha=0.3)

for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.01,
            f'{val:.4f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig("expressibility_gap.png", dpi=150, bbox_inches='tight')
print("  Saved: expressibility_gap.png")

# ── Plot 3: Magnetic field sweep ───────────────────────────────────────────
h_values = np.linspace(0, 2, 10)
exact_energies = []
vqe_shallow_energies = []

print("\n  Running magnetic field sweep...")
for h_val in h_values:
    H_h = build_hamiltonian(J=1, h=h_val)
    exact_energies.append(exact_ground_state(H_h))
    _, hist = run_vqe(H_h, ansatz_fn=shallow_ansatz, n_params=6)
    vqe_shallow_energies.append(hist[-1])

fig3, ax = plt.subplots(figsize=(8, 5))
ax.plot(h_values, exact_energies, 'r--', linewidth=2, label='Exact')
ax.plot(h_values, vqe_shallow_energies, 'o-', color='steelblue',
        linewidth=2, markersize=5, label='VQE (shallow)')
ax.set_xlabel("Magnetic Field (h)", fontsize=12)
ax.set_ylabel("Ground State Energy", fontsize=12)
ax.set_title("Energy vs Magnetic Field — 3-Qubit TFIM", fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("energy_vs_field.png", dpi=150, bbox_inches='tight')
print("  Saved: energy_vs_field.png")
print("\n  Done.")