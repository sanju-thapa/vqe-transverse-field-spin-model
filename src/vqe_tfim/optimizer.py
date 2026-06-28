import numpy as np
from qiskit.quantum_info import Statevector


def energy(theta, hamiltonian, ansatz_fn):
    qc = ansatz_fn(theta)
    state = Statevector(qc)
    return state.expectation_value(hamiltonian).real


def parameter_shift_gradient(theta, hamiltonian, ansatz_fn):
    shift = np.pi / 2
    grad = np.zeros(len(theta))

    for i in range(len(theta)):
        theta_plus = theta.copy()
        theta_plus[i] += shift

        theta_minus = theta.copy()
        theta_minus[i] -= shift

        grad[i] = 0.5 * (
            energy(theta_plus, hamiltonian, ansatz_fn) -
            energy(theta_minus, hamiltonian, ansatz_fn)
        )

    return grad


def run_vqe(hamiltonian, ansatz_fn, n_params, iterations=300, learning_rate=0.05, seed=42):
    rng = np.random.default_rng(seed)
    theta = rng.uniform(0, 2 * np.pi, n_params)
    energy_history = []

    for step in range(iterations):
        e = energy(theta, hamiltonian, ansatz_fn)
        energy_history.append(e)

        grad = parameter_shift_gradient(theta, hamiltonian, ansatz_fn)
        theta = theta - learning_rate * grad

    return theta, energy_history