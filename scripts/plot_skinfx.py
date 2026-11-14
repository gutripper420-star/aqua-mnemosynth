"""Plot an open-boundary skin profile and the Hatano–Nelson GBZ spectrum."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from core.lattice import calculate_com, continuum_on_gbz, hatano_nelson, obc_spectrum


def plot_skin_effect(
    output: Path,
    n: int = 40,
    t: float = 1.0,
    gamma: float = 0.4,
) -> None:
    matrix = hatano_nelson(n, t=t, gamma=gamma)
    _, eigenvectors = np.linalg.eig(matrix)
    centers = calculate_com(eigenvectors)
    state_index = int(np.argmin(centers))
    site_density = np.abs(eigenvectors[:, state_index]) ** 2
    site_density /= site_density.sum()
    _, continuum = continuum_on_gbz(t, gamma)
    finite_spectrum = obc_spectrum(n, t=t, gamma=gamma)

    figure, (skin_axis, spectrum_axis) = plt.subplots(1, 2, figsize=(11, 4.5))
    skin_axis.plot(np.arange(n), site_density, marker=".", linewidth=1)
    skin_axis.set(
        xlabel="Site",
        ylabel="Normalized probability density",
        title=f"Open-boundary skin profile (N={n})",
    )

    spectrum_axis.plot(
        continuum.real,
        continuum.imag,
        color="tab:blue",
        label="Continuum on GBZ",
    )
    spectrum_axis.scatter(
        finite_spectrum.real,
        finite_spectrum.imag,
        color="tab:orange",
        marker="x",
        label="Finite OBC spectrum",
        zorder=3,
    )
    spectrum_axis.set(
        xlabel="Re(E)",
        ylabel="Im(E)",
        title=f"Generalized Brillouin zone (t={t:g}, γ={gamma:g})",
    )
    spectrum_axis.axhline(0, color="0.8", linewidth=0.7)
    spectrum_axis.axvline(0, color="0.8", linewidth=0.7)
    spectrum_axis.legend()
    figure.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=160)
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("skinfx.png"))
    parser.add_argument("--sites", type=int, default=40)
    parser.add_argument("--hopping", type=float, default=1.0)
    parser.add_argument("--asymmetry", type=float, default=0.4)
    args = parser.parse_args()
    plot_skin_effect(args.output, args.sites, args.hopping, args.asymmetry)


if __name__ == "__main__":
    main()
