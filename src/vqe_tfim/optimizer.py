import numpy as np
from qiskit.quantum_info import Statevector
from .ansatz import shallow_ansatz


def energy(theta, hamiltonian):
    """Compute <psi(theta)|H|psi(theta)> for the given parameters."""
    qc = shallow_ansatz(theta)
    state = Statevector(qc)
    return state.expectation_value(hamiltonian).real


def parameter_shift_gradient(theta, hamiltonian):
    """Estimate the gradient of the energy using the parameter-shift rule."""
    shift = np.pi / 2
    grad = np.zeros(len(theta))

    for i in range(len(theta)):
        theta_plus = theta.copy()
        theta_plus[i] += shift

        theta_minus = theta.copy()
        theta_minus[i] -= shift

        grad[i] = 0.5 * (energy(theta_plus, hamiltonian) - energy(theta_minus, hamiltonian))

    return grad


def run_vqe(hamiltonian, n_params=6, iterations=100, learning_rate=0.05):
    """Run gradient descent VQE and return the final parameters and energy history."""
    theta = np.random.uniform(0, 2 * np.pi, n_params)
    energy_history = []

    for step in range(iterations):
        e = energy(theta, hamiltonian)
        energy_history.append(e)

        grad = parameter_shift_gradient(theta, hamiltonian)
        theta = theta - learning_rate * grad

    return theta, energy_history