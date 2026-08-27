"""A one-dimensional constant-velocity Kalman filter learning exercise."""

from __future__ import annotations

import numpy as np


class ConstantVelocityKalman1D:
    """Estimate `[position, velocity]` from noisy position observations.

    This small filter makes SORT's predict/update mechanism inspectable before
    expanding the state to bounding-box center, scale/height, and aspect ratio.
    `process_variance` represents white acceleration-noise variance.
    """

    def __init__(
        self,
        position: float,
        *,
        velocity: float = 0.0,
        covariance: np.ndarray | None = None,
        process_variance: float = 1.0,
    ) -> None:
        # LEARNER TODO: validate finite scalars and a symmetric positive-semidefinite
        # 2x2 covariance, then store float64 state/covariance without aliasing input.
        raise NotImplementedError("implement ConstantVelocityKalman1D.__init__")

    def predict(self, dt: float = 1.0) -> float:
        """Apply constant-velocity motion and white-acceleration process noise.

        Use F=[[1,dt],[0,1]] and
        Q=q*[[dt^4/4,dt^3/2],[dt^3/2,dt^2]]. Return predicted position.
        """
        # LEARNER TODO: validate dt, then update state and covariance.
        raise NotImplementedError("implement ConstantVelocityKalman1D.predict")

    def update(self, measurement: float, measurement_variance: float) -> float:
        """Fuse one finite position measurement and return updated position.

        Use H=[1,0]. Update covariance with the Joseph form so the implementation
        remains symmetric and numerically well behaved.
        """
        # LEARNER TODO: compute innovation, innovation covariance, Kalman gain,
        # posterior state, and Joseph-form posterior covariance.
        raise NotImplementedError("implement ConstantVelocityKalman1D.update")

