from __future__ import annotations

import os

import numpy as np
import pytest

from ml_fundamentals.gradient_checks import (
    central_difference_gradient,
    check_gradient,
    relative_error,
)


pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_ML_EXERCISES") != "1",
    reason="set RUN_ML_EXERCISES=1 to run learner challenges",
)


def test_central_difference_handles_matrix_input_without_mutation() -> None:
    point = np.array([[1.0, -2.0], [0.5, 3.0]])
    original = point.copy()

    numeric = central_difference_gradient(lambda value: float(np.sum(value**3)), point)

    np.testing.assert_allclose(numeric, 3.0 * point**2, rtol=1e-6, atol=1e-7)
    np.testing.assert_array_equal(point, original)


def test_relative_error_is_zero_for_equal_zero_gradients() -> None:
    assert relative_error(np.zeros(3), np.zeros(3)) == pytest.approx(0.0)


def test_relative_error_rejects_mismatched_shapes() -> None:
    with pytest.raises(ValueError):
        relative_error(np.zeros(2), np.zeros(3))


def test_check_gradient_distinguishes_good_and_bad_derivatives() -> None:
    point = np.array([0.2, -0.7, 1.1])
    function = lambda value: float(np.sum(np.sin(value)))

    good = check_gradient(function, point, np.cos(point), tolerance=1e-7)
    bad = check_gradient(function, point, np.ones_like(point), tolerance=1e-7)

    assert good.passed
    assert good.relative_error < 1e-7
    assert not bad.passed
    assert bad.relative_error > good.relative_error
