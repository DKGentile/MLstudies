"""Detection-to-track association exercises."""

from __future__ import annotations

import numpy as np


def greedy_iou_match(
    iou: np.ndarray, threshold: float
) -> tuple[list[tuple[int, int]], list[int], list[int]]:
    """Greedily match rows (tracks) to columns (detections) by descending IoU.

    Each row and column may be used once. Values below `threshold` are ineligible.
    Resolve equal-IoU ties by lower row index, then lower column index. Return
    sorted matches plus sorted unmatched row and column indices.

    This deliberately teaches a simple baseline. Later, construct a matrix where
    greedy assignment is worse than a globally optimal Hungarian assignment.
    """
    # LEARNER TODO: validate the matrix/threshold and implement deterministic matching.
    raise NotImplementedError("implement greedy_iou_match")

