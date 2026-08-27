"""Detector preprocessing exercises that preserve reversible geometry."""

from __future__ import annotations

import numpy as np


def letterbox(
    image: np.ndarray, target_height: int, target_width: int, fill: int = 114
) -> tuple[np.ndarray, float, tuple[int, int]]:
    """Resize with preserved aspect ratio and symmetric-ish integer padding.

    Return `(canvas, scale, (pad_left, pad_top))`. Put any odd extra pixel on the
    right or bottom. Implement nearest-neighbor sampling yourself for this exercise;
    the production pipeline may later switch to OpenCV after parity is tested.
    """
    # LEARNER TODO: validate HWC input, compute scale/padding, and resize by index mapping.
    raise NotImplementedError("implement letterbox")


def scale_boxes_back(
    boxes_xyxy: np.ndarray,
    scale: float,
    pad_left_top: tuple[int, int],
    original_height: int,
    original_width: int,
) -> np.ndarray:
    """Undo letterbox coordinates and clip xyxy boxes to the original image."""
    # LEARNER TODO: subtract padding, divide by scale, and clip x/y independently.
    raise NotImplementedError("implement scale_boxes_back")

