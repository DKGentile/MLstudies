from __future__ import annotations

import os

import numpy as np
import pytest

from ml_fundamentals.regularization import (
    bias_variance,
    polynomial_features,
    ridge_loss_and_gradient,
    train_validation_split,
)


pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_ML_EXERCISES") != "1",
    reason="set RUN_ML_EXERCISES=1 to run learner challenges",
)


def test_polynomial_features_orders_powers_by_column() -> None:
    actual = polynomial_features(np.array([2.0, -1.0]), degree=3)
    expected = np.array([[1.0, 2.0, 4.0, 8.0], [1.0, -1.0, 1.0, -1.0]])
    np.testing.assert_array_equal(actual, expected)


def test_polynomial_features_can_omit_intercept() -> None:
    actual = polynomial_features(np.array([2.0]), degree=3, include_intercept=False)
    np.testing.assert_array_equal(actual, [[2.0, 4.0, 8.0]])


def test_ridge_value_and_gradient_exclude_intercept() -> None:
    x = np.array([[1.0, 1.0], [1.0, 2.0]])
    targets = np.array([2.0, 4.0])
    weights = np.array([1.0, 2.0])

    loss, gradient = ridge_loss_and_gradient(weights, x, targets, strength=0.1)

    assert loss == pytest.approx(0.7)
    np.testing.assert_allclose(gradient, [1.0, 1.7])


def test_bias_variance_uses_model_axis() -> None:
    predictions = np.array([[0.0, 2.0], [2.0, 4.0], [1.0, 3.0]])
    targets = np.array([1.0, 2.0])

    squared_bias, variance = bias_variance(predictions, targets)

    assert squared_bias == pytest.approx(0.5)
    assert variance == pytest.approx(2.0 / 3.0)


def test_split_is_reproducible_aligned_and_nonempty() -> None:
    x = np.arange(20.0).reshape(10, 2)
    targets = np.arange(10.0)

    split_a = train_validation_split(x, targets, validation_fraction=0.3, seed=12)
    split_b = train_validation_split(x, targets, validation_fraction=0.3, seed=12)

    for a, b in zip(split_a, split_b, strict=True):
        np.testing.assert_array_equal(a, b)
    x_train, x_val, y_train, y_val = split_a
    assert x_train.shape[0] == y_train.shape[0] == 7
    assert x_val.shape[0] == y_val.shape[0] == 3
    np.testing.assert_array_equal(x_train[:, 0] / 2.0, y_train)
    np.testing.assert_array_equal(x_val[:, 0] / 2.0, y_val)
