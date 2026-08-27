"""Exercise 5: regularization and empirical bias/variance measurements."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def polynomial_features(
    x: ArrayLike,
    degree: int,
    *,
    include_intercept: bool = True,
) -> NDArray[np.float64]:
    """Expand a one-dimensional input into increasing polynomial powers.

    With an intercept, columns represent powers ``0..degree``. Without one,
    they represent ``1..degree``. Reject non-1-D inputs and degree below one.
    """

    # TODO: use broadcasting or a NumPy polynomial helper, not a sample loop.
    raise NotImplementedError("implement polynomial_features")


def ridge_loss_and_gradient(
    weights: ArrayLike,
    x: ArrayLike,
    targets: ArrayLike,
    *,
    strength: float,
    regularize_intercept: bool = False,
) -> tuple[float, NDArray[np.float64]]:
    """Return MSE plus an L2 penalty and its analytic gradient.

    The data term is ``0.5 * mean((X @ w - y) ** 2)`` and the penalty is
    ``0.5 * strength * sum(w_reg ** 2)``. Weight zero is the intercept.
    """

    # TODO: derive both terms. Do not regularize weight zero unless requested.
    raise NotImplementedError("implement ridge_loss_and_gradient")


def bias_variance(
    predictions: ArrayLike,
    noiseless_targets: ArrayLike,
) -> tuple[float, float]:
    """Return empirical ``(squared_bias, variance)`` across fitted models.

    ``predictions`` has shape ``(models, evaluation_points)`` and targets has
    shape ``(evaluation_points,)``. Average both quantities over evaluation
    points. This deliberately excludes irreducible observation noise.
    """

    # TODO: first average predictions over models; then measure the two distinct
    # sources of error described in the docstring.
    raise NotImplementedError("implement bias_variance")


def train_validation_split(
    x: ArrayLike,
    targets: ArrayLike,
    *,
    validation_fraction: float = 0.25,
    seed: int = 0,
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Shuffle deterministically and return ``x_train, x_val, y_train, y_val``.

    Put ``round(n * validation_fraction)`` samples in validation and reject any
    fraction that would make either partition empty.
    """

    # TODO: create a local Generator from seed and apply one shared permutation
    # to features and targets.
    raise NotImplementedError("implement train_validation_split")
