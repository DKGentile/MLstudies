"""Exercise 2: linear regression and batch gradient descent from scratch."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def add_intercept(x: ArrayLike) -> NDArray[np.float64]:
    """Prepend a column of ones to a 1-D or 2-D feature array."""

    # TODO: make a 1-D feature vector mean ``n samples, one feature`` and reject
    # arrays of every other rank.
    raise NotImplementedError("implement add_intercept")


def mse_loss_and_gradient(
    weights: ArrayLike,
    x: ArrayLike,
    targets: ArrayLike,
) -> tuple[float, NDArray[np.float64]]:
    """Return ``0.5 * mean((X @ w - y) ** 2)`` and its gradient.

    ``x`` is ``(samples, features)``, ``weights`` is ``(features,)``, and
    ``targets`` is ``(samples,)``. Validate compatible, non-empty shapes.
    """

    # TODO: implement the vectorized forward value and analytic gradient. Do
    # not loop over samples.
    raise NotImplementedError("implement mse_loss_and_gradient")


def fit_gradient_descent(
    x: ArrayLike,
    targets: ArrayLike,
    *,
    learning_rate: float = 0.05,
    steps: int = 500,
    initial_weights: ArrayLike | None = None,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Fit linear regression and return ``(weights, loss_history)``.

    Record the loss before every update, so ``loss_history.shape == (steps,)``.
    Do not add an intercept automatically; callers decide whether to use
    :func:`add_intercept`.
    """

    # TODO: initialize deterministically to zeros when initial_weights is None,
    # validate hyperparameters, and repeatedly call mse_loss_and_gradient.
    raise NotImplementedError("implement fit_gradient_descent")


def predict(weights: ArrayLike, x: ArrayLike) -> NDArray[np.float64]:
    """Return linear predictions with shape ``(samples,)``."""

    # TODO: validate shapes and compute the matrix-vector product.
    raise NotImplementedError("implement predict")
