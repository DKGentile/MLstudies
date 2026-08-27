"""Exercise 3: numerically stable binary logistic regression."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def sigmoid(logits: ArrayLike) -> NDArray[np.float64]:
    """Return a numerically stable element-wise sigmoid.

    The result must be finite for all finite float64 inputs, including values
    near the limits of exponentiation.
    """

    # TODO: use separate algebraically equivalent expressions for non-negative
    # and negative inputs so neither branch overflows.
    raise NotImplementedError("implement sigmoid")


def binary_cross_entropy_from_logits(logits: ArrayLike, targets: ArrayLike) -> float:
    """Return mean binary cross entropy directly from logits.

    ``logits`` and ``targets`` must be matching, non-empty 1-D arrays, and every
    target must be exactly zero or one. Avoid taking ``log(0)``.
    """

    # TODO: express BCE using a stable log-sum-exp identity rather than first
    # converting logits to probabilities.
    raise NotImplementedError("implement binary_cross_entropy_from_logits")


def logistic_loss_and_gradient(
    weights: ArrayLike,
    x: ArrayLike,
    targets: ArrayLike,
    *,
    l2: float = 0.0,
    regularize_intercept: bool = False,
) -> tuple[float, NDArray[np.float64]]:
    """Return regularized mean logistic loss and its analytic gradient.

    The penalty added to the data loss is ``0.5 * l2 * sum(w_reg ** 2)``.
    Unless ``regularize_intercept`` is true, weight zero is excluded. Assume
    the caller has put an intercept column in ``x`` when one is desired.
    """

    # TODO: combine the stable BCE objective, analytic data gradient, and L2
    # term. Validate dimensions, binary labels, and non-negative l2.
    raise NotImplementedError("implement logistic_loss_and_gradient")


def fit_gradient_descent(
    x: ArrayLike,
    targets: ArrayLike,
    *,
    learning_rate: float = 0.1,
    steps: int = 500,
    l2: float = 0.0,
    initial_weights: ArrayLike | None = None,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Fit binary logistic regression and return weights plus loss history."""

    # TODO: implement batch gradient descent using
    # logistic_loss_and_gradient. Record each pre-update loss.
    raise NotImplementedError("implement fit_gradient_descent")


def predict_proba(weights: ArrayLike, x: ArrayLike) -> NDArray[np.float64]:
    """Return positive-class probabilities for each row of ``x``."""

    # TODO: validate shapes and reuse sigmoid.
    raise NotImplementedError("implement predict_proba")


def predict(weights: ArrayLike, x: ArrayLike, *, threshold: float = 0.5) -> NDArray[np.int64]:
    """Return binary predictions using ``probability >= threshold``."""

    # TODO: require a threshold in [0, 1] and return integer labels.
    raise NotImplementedError("implement predict")
