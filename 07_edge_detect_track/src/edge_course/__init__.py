"""Learner-implemented evaluation and tracking primitives for the capstone."""

from .geometry import box_iou_matrix
from .kalman import ConstantVelocityKalman1D
from .matching import greedy_iou_match
from .metrics import interpolated_average_precision, precision_recall_curve
from .tracker import Detection, IoUTracker, Track

__all__ = [
    "Detection",
    "ConstantVelocityKalman1D",
    "IoUTracker",
    "Track",
    "box_iou_matrix",
    "greedy_iou_match",
    "interpolated_average_precision",
    "precision_recall_curve",
]
