"""Exercise 6: a tiny affine-ReLU-affine classifier with manual backprop."""

from __future__ import annotations

from typing import TypeAlias

import numpy as np
from numpy.typing import ArrayLike, NDArray


Parameters: TypeAlias = dict[str, NDArray[np.float64]]
Cache: TypeAlias = dict[str, NDArray[np.float64]]


def initialize_parameters(
    input_dim: int,
    hidden_dim: int,
    output_dim: int,
    *,
    seed: int = 0,
) -> Parameters:
    """Create ``W1, b1, W2, b2`` with deterministic small random weights.

    Biases start at zero. Draw weights from a standard normal using
    ``np.random.default_rng(seed)`` and scale them by ``0.01``.
    """

    # TODO: validate positive dimensions and return arrays with conventional
    # row-major affine-layer shapes.
    raise NotImplementedError("implement initialize_parameters")


def forward(parameters: Parameters, x: ArrayLike) -> tuple[NDArray[np.float64], Cache]:
    """Run affine-ReLU-affine and return ``(logits, cache)``.

    Cache exactly the arrays your backward implementation needs. Input has
    shape ``(batch, input_dim)`` and logits has shape ``(batch, output_dim)``.
    """

    # TODO: validate parameter compatibility, compute the two affine stages,
    # and apply ReLU between them.
    raise NotImplementedError("implement forward")


def softmax_cross_entropy(
    logits: ArrayLike,
    labels: ArrayLike,
) -> tuple[float, NDArray[np.float64]]:
    """Return mean softmax cross-entropy and its gradient with respect to logits.

    ``labels`` contains one integer class index per row. The implementation must
    be stable for large finite logits and must not mutate either input.
    """

    # TODO: derive the log-sum-exp forward value and the batch-averaged gradient
    # with respect to every logit.
    raise NotImplementedError("implement softmax_cross_entropy")


def backward(
    parameters: Parameters,
    cache: Cache,
    dlogits: ArrayLike,
    *,
    l2: float = 0.0,
) -> Parameters:
    """Backpropagate through the network and return gradients by parameter name.

    Add ``0.5 * l2 * (sum(W1**2) + sum(W2**2))`` to the objective represented
    by the returned gradients. Biases are not regularized.
    """

    # TODO: work backward through affine 2, the ReLU mask, and affine 1. Ensure
    # every returned gradient has the same shape as its parameter.
    raise NotImplementedError("implement backward")


def loss_and_gradients(
    parameters: Parameters,
    x: ArrayLike,
    labels: ArrayLike,
    *,
    l2: float = 0.0,
) -> tuple[float, Parameters]:
    """Compose forward, softmax loss, L2 loss, and backward propagation."""

    # TODO: this should be a short composition of the functions above. Include
    # the L2 value exactly once and pass its gradient responsibility backward.
    raise NotImplementedError("implement loss_and_gradients")


def gradient_descent_step(
    parameters: Parameters,
    gradients: Parameters,
    *,
    learning_rate: float,
) -> Parameters:
    """Return updated parameter copies without mutating either input mapping."""

    # TODO: validate matching keys/shapes and a positive learning rate.
    raise NotImplementedError("implement gradient_descent_step")
