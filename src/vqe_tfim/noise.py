"""
Noisy VQE simulation using a real-hardware noise model.

Uses qiskit-aer's AerSimulator with a NoiseModel derived from a
FakeManilaV2 calibration snapshot (real IBM device noise: gate errors,
readout errors, decoherence times). Energy is estimated via finite-shot
Pauli-term measurement, not exact statevector expectation.
"""
import numpy as np
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime.fake_provider import FakeManilaV2

_backend = FakeManilaV2()
_noise_model = NoiseModel.from_backend(_backend)
_sim = AerSimulator(noise_model=_noise_model)


def _build_measurement_circuits(theta, ansatz_fn, pauli_labels):
    qc = ansatz_fn(theta)
    circuits = []
    for label in pauli_labels:
        meas_qc = qc.copy()
        for i, p in enumerate(reversed(label)):
            if p == 'X':
                meas_qc.h(i)
            elif p == 'Y':
                meas_qc.sdg(i)
                meas_qc.h(i)
        meas_qc.measure_all()
        circuits.append(meas_qc)
    return circuits


def noisy_energy(theta, ansatz_fn, hamiltonian, shots=512):
    """Estimate <psi(theta)|H|psi(theta)> under FakeManilaV2 noise, batched."""
    pauli_labels = hamiltonian.paulis.to_labels()
    coeffs = [c.real for c in hamiltonian.coeffs]

    circuits = _build_measurement_circuits(theta, ansatz_fn, pauli_labels)
    transpiled = transpile(circuits, _sim, optimization_level=1)
    results = _sim.run(transpiled, shots=shots).result()

    total = 0.0
    for idx, label in enumerate(pauli_labels):
        counts = results.get_counts(idx)
        n_shots = sum(counts.values())
        rev_label = label[::-1]
        exp = 0.0
        for bitstring, count in counts.items():
            bits = bitstring.replace(' ', '')
            parity = 1
            for i, p in enumerate(rev_label):
                if p != 'I':
                    bit = int(bits[-(i + 1)])
                    parity *= (1 - 2 * bit)
            exp += parity * count
        exp /= n_shots
        total += coeffs[idx] * exp
    return total


def noisy_gradient(theta, ansatz_fn, hamiltonian, shots=512):
    """Parameter-shift gradient using noisy energy estimates."""
    shift = np.pi / 2
    grad = np.zeros(len(theta))
    for i in range(len(theta)):
        tp = theta.copy()
        tp[i] += shift
        tm = theta.copy()
        tm[i] -= shift
        grad[i] = 0.5 * (
            noisy_energy(tp, ansatz_fn, hamiltonian, shots)
            - noisy_energy(tm, ansatz_fn, hamiltonian, shots)
        )
    return grad


def run_noisy_vqe(hamiltonian, ansatz_fn, n_params, iterations=60,
                   lr=0.05, shots=512, seed=42):
    """
    Gradient-descent VQE loop under FakeManilaV2 noise.

    Note: iterations defaults to 60, not 300 (as in the noiseless
    run_vqe), purely for runtime cost — each iteration requires
    2*n_params + 1 batched noisy circuit evaluations. Normalize any
    area-under-curve comparison against the noiseless run by
    iteration count before comparing the two.
    """
    rng = np.random.default_rng(seed)
    theta = rng.uniform(0, 2 * np.pi, n_params)
    history = []
    for _ in range(iterations):
        e = noisy_energy(theta, ansatz_fn, hamiltonian, shots)
        history.append(e)
        grad = noisy_gradient(theta, ansatz_fn, hamiltonian, shots)
        theta = theta - lr * grad
    return theta, history