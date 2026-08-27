from __future__ import annotations

import os

import numpy as np
import pytest

from ml_fundamentals.linear_regression import (
    add_intercept,
    fit_gradient_descent,
    mse_loss_and_gradient,
    predict,
)


pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_ML_EXERCISES") != "1",
    reason="set RUN_ML_EXERCISES=1 to run learner challenges",
)


def _central_difference(function, point: np.ndarray, epsilon: float = 1e-6) -> np.ndarray:
    result = np.zeros_like(point, dtype=float)
    for index in range(point.size):
        plus = point.copy()
        minus = point.copy()
        plus[index] += epsilon
        minus[index] -= epsilon
        result[index] = (function(plus) - function(minus)) / (2.0 * epsilon)
    return result


def test_add_intercept_supports_vector_and_matrix() -> None:
    np.testing.assert_array_equal(add_intercept([2.0, 4.0]), [[1.0, 2.0], [1.0, 4.0]])
    np.testing.assert_array_equal(
        add_intercept([[2.0, 3.0], [4.0, 5.0]]),
        [[1.0, 2.0, 3.0], [1.0, 4.0, 5.0]],
    )


def test_mse_value_and_gradient_on_small_example() -> None:
    x = np.array([[1.0, 1.0], [1.0, 2.0]])
    targets = np.array([3.0, 5.0])

    loss, gradient = mse_loss_and_gradient(np.zeros(2), x, targets)

    assert loss == pytest.approx(8.5)
    np.testing.assert_allclose(gradient, [-4.0, -6.5])


def test_mse_gradient_matches_central_difference() -> None:
    rng = np.random.default_rng(42)
    x = rng.normal(size=(7, 3))
    targets = rng.normal(size=7)
    weights = rng.normal(size=3)

    _, analytic = mse_loss_and_gradient(weights, x, targets)
    numeric = _central_difference(lambda w: mse_loss_and_gradient(w, x, targets)[0], weights)

    np.testing.assert_allclose(analytic, numeric, rtol=1e-6, atol=1e-7)


def test_gradient_descent_recovers_noiseless_line() -> None:
    feature = np.linspace(-2.0, 2.0, 21)
    x = add_intercept(feature)
    targets = 1.5 + 2.0 * feature

    weights, history = fit_gradient_descent(x, targets, learning_rate=0.1, steps=300)

    np.testing.assert_allclose(weights, [1.5, 2.0], atol=1e-5)
    assert history.shape == (300,)
    assert history[-1] < history[0]
    np.testing.assert_allclose(predict(weights, x), targets, atol=1e-5)
