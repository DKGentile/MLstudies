"""Exercise 4: finite differences as a debugging instrument."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from numpy.typing import ArrayLike, NDArray


ScalarFunction = Callable[[NDArray[np.float64]], float]


@dataclass(frozen=True)
class GradientCheckResult:
    """Summary returned by :func:`check_gradient`."""

    passed: bool
    relative_error: float
    numeric: NDArray[np.float64]
    analytic: NDArray[np.float64]


def central_difference_gradient(
    function: ScalarFunction,
    point: ArrayLike,
    *,
    epsilon: float = 1e-5,
) -> NDArray[np.float64]:
    """Estimate every partial derivative at ``point`` with central differences.

    Do not mutate the caller's array. ``function`` may accept an array of any
    shape but must return a scalar.
    """

    # TODO: iterate over arbitrary-dimensional indices and perturb one element
    # in each direction. Validate epsilon and scalar outputs.
    raise NotImplementedError("implement central_difference_gradient")


def relative_error(analytic: ArrayLike, numeric: ArrayLike) -> float:
    """Return a scale-aware maximum relative error for two gradients.

    Use a denominator that remains meaningful when both compared values are
    near zero. Matching empty arrays are invalid.
    """

    # TODO: validate matching shapes and define a small absolute floor for the
    # denominator.
    raise NotImplementedError("implement relative_error")


def check_gradient(
    function: ScalarFunction,
    point: ArrayLike,
    analytic_gradient: ArrayLike,
    *,
    epsilon: float = 1e-5,
    tolerance: float = 1e-6,
) -> GradientCheckResult:
    """Compare an analytic gradient with a finite-difference estimate."""

    # TODO: validate tolerance, call the two helpers, and populate the result.
    raise NotImplementedError("implement check_gradient")
