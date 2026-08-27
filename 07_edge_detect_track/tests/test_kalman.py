from __future__ import annotations

import numpy as np
import pytest

from edge_course.kalman import ConstantVelocityKalman1D


pytestmark = pytest.mark.exercise


def test_prediction_advances_position_and_covariance() -> None:
    tracker = ConstantVelocityKalman1D(
        2.0,
        velocity=3.0,
        covariance=np.eye(2),
        process_variance=0.0,
    )
    assert tracker.predict(dt=2.0) == pytest.approx(8.0)
    np.testing.assert_allclose(tracker.state, [8.0, 3.0])
    np.testing.assert_allclose(tracker.covariance, [[5.0, 2.0], [2.0, 1.0]])


def test_measurement_updates_position_and_velocity() -> None:
    tracker = ConstantVelocityKalman1D(
        0.0, covariance=np.eye(2), process_variance=0.0
    )
    tracker.predict(dt=1.0)
    assert tracker.update(measurement=2.0, measurement_variance=1.0) == pytest.approx(4 / 3)
    np.testing.assert_allclose(tracker.state, [4 / 3, 2 / 3])
    np.testing.assert_allclose(tracker.covariance, [[2 / 3, 1 / 3], [1 / 3, 2 / 3]])


def test_repeated_updates_reduce_position_uncertainty() -> None:
    tracker = ConstantVelocityKalman1D(0.0, process_variance=0.01)
    before = tracker.covariance[0, 0]
    for measurement in [0.8, 2.2, 2.9, 4.1]:
        tracker.predict()
        tracker.update(measurement, measurement_variance=0.25)
    assert tracker.covariance[0, 0] < before
    assert np.isfinite(tracker.state).all()


@pytest.mark.parametrize("dt", [0.0, -1.0, float("nan")])
def test_predict_rejects_invalid_time_step(dt: float) -> None:
    tracker = ConstantVelocityKalman1D(0.0)
    with pytest.raises(ValueError):
        tracker.predict(dt)

