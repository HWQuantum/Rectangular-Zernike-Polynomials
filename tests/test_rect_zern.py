#!/usr/bin/env python
"""Tests for `rect_zern` package."""

import pytest
import numpy as np

from rect_zern import rect_zern


def test_coefficients_are_generated_correctly():
    assert [(0, 0), (-1, 1), (1, 1)] == list(rect_zern.coefficients(3))


def test_rectangular_zernike_modes_gives_correct_number_of_modes():
    n_modes = 4
    shape = (200, 300)
    (modes, x, y) = rect_zern.rectangular_zernike_modes(n_modes, *shape)
    assert x.shape == shape
    assert y.shape == shape
    assert len(modes) == n_modes
    assert modes[0].shape == shape


def test_rectangular_zernike_modes_are_orthonormal():
    dim = 4
    (modes, _, _) = rect_zern.rectangular_zernike_modes(dim, 200, 300)
    assert np.all(
        np.isclose(
            np.array([[(i * j.conj()).sum() for i in modes] for j in modes]),
            np.eye(dim) / np.pi))
