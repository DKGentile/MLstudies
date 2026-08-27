from __future__ import annotations

import numpy as np
import pytest

from edge_course.metrics import interpolated_average_precision, precision_recall_curve


pytestmark = pytest.mark.exercise


def test_precision_recall_sorts_by_descending_score() -> None:
    scores = np.array([0.4, 0.9, 0.7])
    true_positive = np.array([True, True, False])
    precision, recall = precision_recall_curve(scores, true_positive, num_ground_truth=2)
    np.testing.assert_allclose(precision, [1.0, 0.5, 2.0 / 3.0])
    np.testing.assert_allclose(recall, [0.5, 0.5, 1.0])


def test_tied_scores_keep_input_order() -> None:
    precision, recall = precision_recall_curve(
        np.array([0.5, 0.5]), np.array([False, True]), num_ground_truth=1
    )
    np.testing.assert_allclose(precision, [0.0, 0.5])
    np.testing.assert_allclose(recall, [0.0, 1.0])


def test_interpolated_ap_for_perfect_detector() -> None:
    recall = np.array([0.5, 1.0])
    precision = np.array([1.0, 1.0])
    assert interpolated_average_precision(recall, precision) == pytest.approx(1.0)


def test_interpolated_ap_uses_precision_envelope() -> None:
    recall = np.array([0.25, 0.5, 1.0])
    precision = np.array([1.0, 0.5, 0.25])
    # Eleven points make the hand calculation visible: r=0..0.2 -> 1,
    # r=0.3..0.5 -> .5, and r=0.6..1 -> .25.
    assert interpolated_average_precision(recall, precision, points=11) == pytest.approx(
        (3 * 1.0 + 3 * 0.5 + 5 * 0.25) / 11
    )

