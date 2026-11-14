"""Utilities for the one-dimensional Hatano–Nelson lattice."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def _validate_parameters(t: float, gamma: float) -> None:
    if not np.isfinite(t) or not np.isfinite(gamma):
        raise ValueError("t and gamma must be finite real numbers.")


def hatano_nelson(
    n: int,
    t: float = 1.0,
    gamma: float = 0.0,
    *,
    periodic: bool = False,
) -> NDArray[np.float64]:
    """Return the N-site Hatano–Nelson matrix with real asymmetric hopping.

    The upper diagonal is ``t + gamma`` and the lower diagonal is
    ``t - gamma``. Open boundary conditions are used unless ``periodic=True``.
    """
    _validate_parameters(t, gamma)
    if isinstance(n, bool) or not isinstance(n, (int, np.integer)) or n < 1:
        raise ValueError("n must be a positive integer.")

    matrix = np.zeros((n, n), dtype=float)
    indices = np.arange(n - 1)
    matrix[indices, indices + 1] = t + gamma
    matrix[indices + 1, indices] = t - gamma
    if periodic and n > 2:
        matrix[0, n - 1] = t - gamma
        matrix[n - 1, 0] = t + gamma
    elif periodic and n == 2:
        matrix[0, 1] += t - gamma
        matrix[1, 0] += t + gamma
    return matrix


def gbz_radius(t: float, gamma: float) -> float:
    """Return the generalized Brillouin zone radius for real hoppings."""
    _validate_parameters(t, gamma)
    denominator = t + gamma
    if denominator == 0:
        raise ValueError("The GBZ radius is undefined when t + gamma is zero.")
    return float(np.sqrt(abs((t - gamma) / denominator)))


def calculate_com(
    eigenvectors: NDArray[np.complexfloating] | NDArray[np.floating],
) -> float | NDArray[np.float64]:
    """Calculate normalized site-coordinate centers of mass.

    A one-dimensional input is treated as one state. For a two-dimensional
    array, each column is treated as a state and one center is returned per
    column. Sites are indexed from zero.
    """
    states = np.asarray(eigenvectors)
    if states.ndim not in (1, 2) or states.shape[0] == 0:
        raise ValueError("eigenvectors must be a non-empty vector or matrix.")
    if states.ndim == 2 and states.shape[1] == 0:
        raise ValueError("eigenvectors must contain at least one state.")
    if not np.all(np.isfinite(states)):
        raise ValueError("eigenvectors must contain only finite values.")

    weights = np.abs(states) ** 2
    if states.ndim == 1:
        weights = weights[:, None]
    norms = np.sum(weights, axis=0)
    if np.any(norms == 0):
        raise ValueError("Every state must have non-zero norm.")
    coordinates = np.arange(states.shape[0], dtype=float)
    centers = np.sum(coordinates[:, None] * weights, axis=0) / norms
    if states.ndim == 1:
        return float(centers[0])
    return centers


def obc_spectrum(
    n: int,
    t: float = 1.0,
    gamma: float = 0.0,
) -> NDArray[np.complex128]:
    """Return eigenvalues of the N-site matrix with open boundaries."""
    return np.linalg.eigvals(hatano_nelson(n, t, gamma))


def continuum_on_gbz(
    t: float,
    gamma: float,
    num_points: int = 400,
) -> tuple[NDArray[np.float64], NDArray[np.complex128]]:
    """Return momentum samples and the bulk band evaluated on the GBZ.

    The dispersion is ``E = (t + gamma) beta + (t - gamma) / beta`` with
    ``beta = r exp(i k)`` and ``r = gbz_radius(t, gamma)``.
    """
    radius = gbz_radius(t, gamma)
    if isinstance(num_points, bool) or not isinstance(
        num_points, (int, np.integer)
    ) or num_points < 2:
        raise ValueError("num_points must be an integer of at least two.")
    if radius == 0:
        raise ValueError("The GBZ radius must be non-zero.")

    momentum = np.linspace(0.0, 2.0 * np.pi, num_points, endpoint=False)
    beta = radius * np.exp(1j * momentum)
    energies = (t + gamma) * beta + (t - gamma) / beta
    return momentum, np.asarray(energies, dtype=np.complex128)
