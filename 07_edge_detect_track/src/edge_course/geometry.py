"""Bounding-box geometry using the xyxy convention."""

from __future__ import annotations

import numpy as np


def box_iou_matrix(boxes_a: np.ndarray, boxes_b: np.ndarray) -> np.ndarray:
    """Return pairwise IoU with shape `(len(boxes_a), len(boxes_b))`.

    Inputs are float arrays in `[x_min, y_min, x_max, y_max]` order. Degenerate
    boxes have zero area. Reject malformed shapes or coordinates where max < min.
    The result must be finite, including when both boxes have zero area.
    """
    # LEARNER TODO: validate shapes, vectorize intersection/union, and avoid 0/0.
    raise NotImplementedError("implement box_iou_matrix")

