from __future__ import annotations

import os

import numpy as np
import pytest

from ml_fundamentals.two_layer_net import (
    forward,
    gradient_descent_step,
    initialize_parameters,
    loss_and_gradients,
    softmax_cross_entropy,
)


pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_ML_EXERCISES") != "1",
    reason="set RUN_ML_EXERCISES=1 to run learner challenges",
)


def _fixed_problem():
    parameters = {
        "W1": np.array([[0.3, -0.4], [0.2, 0.5]]),
        "b1": np.array([0.1, -0.2]),
        "W2": np.array([[0.7, -0.3, 0.2], [-0.6, 0.4, 0.8]]),
        "b2": np.array([0.05, -0.1, 0.2]),
    }
    x = np.array([[0.5, -1.0], [1.5, 0.7], [-0.3, 2.0]])
    labels = np.array([0, 2, 1])
    return parameters, x, labels


def test_parameter_initialization_is_reproducible_and_well_shaped() -> None:
    first = initialize_parameters(4, 5, 3, seed=9)
    second = initialize_parameters(4, 5, 3, seed=9)

    assert {name: value.shape for name, value in first.items()} == {
        "W1": (4, 5),
        "b1": (5,),
        "W2": (5, 3),
        "b2": (3,),
    }
    for name in first:
        np.testing.assert_array_equal(first[name], second[name])
    np.testing.assert_array_equal(first["b1"], np.zeros(5))
    np.testing.assert_array_equal(first["b2"], np.zeros(3))


def test_forward_applies_relu_between_affine_layers() -> None:
    parameters = {
        "W1": np.array([[1.0, -1.0], [2.0, 1.0]]),
        "b1": np.array([0.0, 0.5]),
        "W2": np.array([[1.0, 2.0], [-1.0, 3.0]]),
        "b2": np.array([0.25, -0.25]),
    }
    x = np.array([[1.0, -1.0], [2.0, 1.0]])

    logits, cache = forward(parameters, x)

    np.testing.assert_allclose(logits, [[0.25, -0.25], [4.25, 7.75]])
    assert cache


def test_softmax_cross_entropy_returns_batch_averaged_gradient() -> None:
    logits = np.zeros((2, 2))
    labels = np.array([0, 1])

    loss, gradient = softmax_cross_entropy(logits, labels)

    assert loss == pytest.approx(np.log(2.0))
    np.testing.assert_allclose(gradient, [[-0.25, 0.25], [0.25, -0.25]])


@pytest.mark.parametrize("parameter_name", ["W1", "b1", "W2", "b2"])
def test_backprop_matches_finite_differences(parameter_name: str) -> None:
    parameters, x, labels = _fixed_problem()
    loss, gradients = loss_and_gradients(parameters, x, labels, l2=0.07)
    assert np.isfinite(loss)
    numeric = np.zeros_like(parameters[parameter_name])
    epsilon = 1e-5

    for index in np.ndindex(numeric.shape):
        plus = {name: value.copy() for name, value in parameters.items()}
        minus = {name: value.copy() for name, value in parameters.items()}
        plus[parameter_name][index] += epsilon
        minus[parameter_name][index] -= epsilon
        plus_loss = loss_and_gradients(plus, x, labels, l2=0.07)[0]
        minus_loss = loss_and_gradients(minus, x, labels, l2=0.07)[0]
        numeric[index] = (plus_loss - minus_loss) / (2.0 * epsilon)

    np.testing.assert_allclose(gradients[parameter_name], numeric, rtol=2e-5, atol=2e-7)


def test_one_small_gradient_step_reduces_loss_without_mutation() -> None:
    parameters, x, labels = _fixed_problem()
    originals = {name: value.copy() for name, value in parameters.items()}
    before, gradients = loss_and_gradients(parameters, x, labels)

    updated = gradient_descent_step(parameters, gradients, learning_rate=0.05)
    after, _ = loss_and_gradients(updated, x, labels)

    assert after < before
    for name in parameters:
        np.testing.assert_array_equal(parameters[name], originals[name])
