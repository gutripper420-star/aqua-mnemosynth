import numpy as np
import pytest

from core.lattice import (
    calculate_com,
    continuum_on_gbz,
    gbz_radius,
    hatano_nelson,
    obc_spectrum,
)


def test_hatano_nelson_hopping_entries():
    matrix = hatano_nelson(4, t=1.0, gamma=0.4)

    np.testing.assert_allclose(np.diag(matrix, 1), 1.4)
    np.testing.assert_allclose(np.diag(matrix, -1), 0.6)
    assert np.count_nonzero(matrix) == 6


def test_hatano_nelson_periodic_boundaries():
    matrix = hatano_nelson(4, t=1.0, gamma=0.4, periodic=True)

    assert matrix[0, -1] == pytest.approx(0.6)
    assert matrix[-1, 0] == pytest.approx(1.4)


def test_gbz_radius_matches_analytic_expression():
    assert gbz_radius(1.0, 0.4) == pytest.approx(np.sqrt(0.6 / 1.4))


def test_obc_spectrum_is_real_for_subcritical_asymmetry():
    spectrum = obc_spectrum(30, t=1.0, gamma=0.4)

    assert np.max(np.abs(spectrum.imag)) < 1e-10


def test_calculate_com_for_vector_and_columns():
    vector_com = calculate_com(np.array([1.0, 0.0, 0.0]))
    column_coms = calculate_com(np.eye(3))

    assert vector_com == pytest.approx(0.0)
    np.testing.assert_allclose(column_coms, [0.0, 1.0, 2.0])


def test_continuum_on_gbz_is_real_for_subcritical_asymmetry():
    momentum, energies = continuum_on_gbz(1.0, 0.4, num_points=100)

    assert momentum.shape == energies.shape == (100,)
    assert np.max(np.abs(energies.imag)) < 1e-12


@pytest.mark.parametrize(
    ("function", "args"),
    [
        (hatano_nelson, (0,)),
        (gbz_radius, (1.0, -1.0)),
        (continuum_on_gbz, (1.0, 1.0)),
    ],
)
def test_invalid_lattice_parameters_raise(function, args):
    with pytest.raises(ValueError):
        function(*args)
