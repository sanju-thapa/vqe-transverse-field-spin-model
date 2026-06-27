# VQE Simulation of the Transverse Field Ising Model

A Python implementation of the **Variational Quantum Eigensolver (VQE)** applied to a three-qubit **Transverse Field Ising Model (TFIM)** — built with Qiskit as part of an M.Sc. Physics thesis at Dr. N.G.P. Arts and Science College (Bharathiar University), 2024–2026.

---

## What This Project Does

This project estimates the **ground state energy** of a quantum spin system using a hybrid quantum–classical optimization loop. Two ansatz circuit architectures (shallow and expressive) are compared in terms of convergence behaviour, energy accuracy, and parameter optimization.

The central finding: both ansatz circuits converge to the same ground state energy (**−2.3138 Hartree**), but the expressive ansatz explores the energy landscape more effectively — quantified by the area under the convergence curve.

---

## The Physics

The Hamiltonian of the three-qubit TFIM is:

```
H = J(Z₁Z₂ + Z₂Z₃) + h(X₁ + X₂ + X₃)
```

- `J` — spin-spin coupling strength between neighbouring qubits
- `h` — transverse magnetic field strength
- `Z`, `X` — Pauli operators acting on individual qubits

The first term models nearest-neighbour spin interactions. The second term represents a transverse magnetic field that drives quantum fluctuations between spin states.

**Default simulation parameters:** `J = 1.0`, `h = 0.5`

---

## Ansatz Circuits

Two parameterized circuit architectures were implemented and compared:

### Shallow Ansatz (6 parameters)
```
H⊗³ → RY(θ₀,θ₁,θ₂) → CNOT(0,1) → CNOT(1,2) → RY(θ₃,θ₄,θ₅)
```
- Superposition layer (Hadamard on all qubits)
- Parameterized RY rotations
- CNOT entanglement chain
- Second RY rotation layer

### Expressive Ansatz (9 parameters)
Extends the shallow circuit with an additional entanglement layer and rotation block — giving the optimizer more freedom to explore the Hilbert space.

---

## Optimization Method

- **Algorithm:** Gradient descent
- **Gradient evaluation:** Parameter-shift rule
- **Learning rate:** 0.05
- **Iterations:** 300
- **Simulator:** Qiskit `Statevector` (noiseless exact simulation)

The parameter-shift rule computes exact gradients from quantum circuits without classical automatic differentiation:

```
∂E/∂θₖ = ½ [ E(θₖ + π/2) − E(θₖ − π/2) ]
```

---

## Key Results

| Metric | Shallow Ansatz | Expressive Ansatz |
|---|---|---|
| Ground state energy | −2.3138 | −2.3138 |
| Area under convergence curve | −165.71 | −172.32 |
| Trainable parameters | 6 | 9 |

Both circuits converge to the same ground state energy, confirming stable VQE optimization. The expressive ansatz achieves a lower area under convergence (more negative), indicating it explores the energy landscape more thoroughly during optimization.

---

## Project Structure

```
vqe-transverse-field-spin-model/
│
├── src/
│   └── vqe_tfim/
│       ├── hamiltonian.py      # Builds the TFIM Hamiltonian as SparsePauliOp
│       ├── ansatz.py           # Shallow and expressive ansatz circuits
│       ├── optimizer.py        # Gradient descent + parameter-shift rule
│       └── exact_solver.py     # Exact diagonalization benchmark
│
├── main.py                     # Entry point — runs VQE and prints results
├── requirements.txt
└── README.md
```

---

## Quickstart

```bash
# Clone the repo
git clone https://github.com/sanju-thapa/vqe-transverse-field-spin-model.git
cd vqe-transverse-field-spin-model

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

**Expected output:**
```
VQE final energy:    -2.3137749048284024
Exact ground energy: -2.3137749048284024
Difference:          ~0.0
Last 10 energy values: [converged values near -2.3138]
```

---

## Dependencies

```
qiskit>=2.0
qiskit-aer
numpy
matplotlib
scipy
```

---

## Background

This project was developed as an M.Sc. Physics thesis (2024–2026) under the guidance of **Dr. R. Dilip**, Department of Physics, Dr. N.G.P. Arts and Science College, Coimbatore, affiliated to Bharathiar University.

The work draws on research experience from a quantum computing internship at **IISc Bangalore** (Centre for High Energy Physics).

---

## References

- Peruzzo et al. (2014) — *A variational eigenvalue solver on a photonic chip*, Nature Communications
- Farhi et al. (2014) — *A Quantum Approximate Optimization Algorithm*
- Mitarai et al. (2018) — *Quantum circuit learning* (parameter-shift rule)
- Qiskit Documentation — https://docs.quantum.ibm.com