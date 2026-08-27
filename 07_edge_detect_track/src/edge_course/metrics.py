"""Small detection-metric exercises independent of a training framework."""

from __future__ import annotations

import numpy as np


def precision_recall_curve(
    scores: np.ndarray, is_true_positive: np.ndarray, num_ground_truth: int
) -> tuple[np.ndarray, np.ndarray]:
    """Return precision and recall after each detection, ordered by score.

    `is_true_positive` is a boolean vector created after one-to-one matching at a
    chosen IoU threshold. Equal scores must retain input order. False detections
    contribute to the precision denominator; `num_ground_truth` sets recall.
    """
    # LEARNER TODO: validate inputs, stable-sort descending, and use cumulative sums.
    raise NotImplementedError("implement precision_recall_curve")


def interpolated_average_precision(
    recall: np.ndarray, precision: np.ndarray, points: int = 101
) -> float:
    """Compute fixed-point interpolated AP over recall levels from 0 through 1.

    At each level use the maximum precision observed at any greater-or-equal
    recall. A level with no qualifying recall contributes zero.
    """
    # LEARNER TODO: implement the precision envelope sampling definition.
    raise NotImplementedError("implement interpolated_average_precision")

