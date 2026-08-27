from __future__ import annotations

import os

import numpy as np
import pytest

from ml_fundamentals.logistic_regression import (
    binary_cross_entropy_from_logits,
    fit_gradient_descent,
    logistic_loss_and_gradient,
    predict,
    predict_proba,
    sigmoid,
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


def test_sigmoid_handles_extreme_logits_without_overflow() -> None:
    probabilities = sigmoid(np.array([-1_000.0, 0.0, 1_000.0]))

    assert np.isfinite(probabilities).all()
    assert probabilities[0] == pytest.approx(0.0, abs=1e-14)
    assert probabilities[1] == pytest.approx(0.5)
    assert probabilities[2] == pytest.approx(1.0, abs=1e-14)


def test_binary_cross_entropy_at_zero_logits() -> None:
    actual = binary_cross_entropy_from_logits(np.zeros(4), np.array([0, 1, 1, 0]))
    assert actual == pytest.approx(np.log(2.0))


def test_regularized_logistic_gradient_matches_finite_difference() -> None:
    rng = np.random.default_rng(7)
    x = np.column_stack((np.ones(9), rng.normal(size=(9, 2))))
    targets = (rng.uniform(size=9) > 0.4).astype(int)
    weights = rng.normal(size=3)

    _, analytic = logistic_loss_and_gradient(weights, x, targets, l2=0.3)
    numeric = _central_difference(
        lambda w: logistic_loss_and_gradient(w, x, targets, l2=0.3)[0],
        weights,
    )

    np.testing.assert_allclose(analytic, numeric, rtol=1e-5, atol=1e-7)


def test_l2_excludes_intercept_by_default() -> None:
    x = np.array([[1.0, -1.0], [1.0, 1.0]])
    targets = np.array([0, 1])
    weights = np.array([2.0, 3.0])

    base_loss, base_gradient = logistic_loss_and_gradient(weights, x, targets)
    loss, gradient = logistic_loss_and_gradient(weights, x, targets, l2=0.5)

    assert loss - base_loss == pytest.approx(0.5 * 0.5 * weights[1] ** 2)
    assert gradient[0] == pytest.approx(base_gradient[0])
    assert gradient[1] - base_gradient[1] == pytest.approx(0.5 * weights[1])


def test_gradient_descent_separates_tiny_dataset() -> None:
    feature = np.array([-2.0, -1.0, -0.5, 0.5, 1.0, 2.0])
    x = np.column_stack((np.ones(feature.size), feature))
    targets = np.array([0, 0, 0, 1, 1, 1])

    weights, history = fit_gradient_descent(x, targets, learning_rate=0.3, steps=250)

    np.testing.assert_array_equal(predict(weights, x), targets)
    assert np.all((predict_proba(weights, x) >= 0.0) & (predict_proba(weights, x) <= 1.0))
    assert history[-1] < history[0]


def test_predict_rejects_invalid_threshold() -> None:
    with pytest.raises(ValueError):
        predict(np.zeros(2), np.ones((1, 2)), threshold=1.1)
