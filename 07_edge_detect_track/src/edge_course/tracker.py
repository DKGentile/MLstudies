"""A small IoU tracker whose lifecycle you implement before studying SORT."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .geometry import box_iou_matrix
from .matching import greedy_iou_match


@dataclass(frozen=True)
class Detection:
    box: tuple[float, float, float, float]
    score: float
    class_id: int


@dataclass
class Track:
    track_id: int
    box: tuple[float, float, float, float]
    score: float
    class_id: int
    age: int = 1
    hits: int = 1
    missed: int = 0


class IoUTracker:
    """Constant-box tracker with class-aware IoU association.

    This is not full SORT: there is no Kalman motion model. It isolates association
    and lifecycle rules so their failure modes are visible first.
    """

    def __init__(self, iou_threshold: float = 0.3, max_missed: int = 2) -> None:
        if not 0.0 <= iou_threshold <= 1.0:
            raise ValueError("iou_threshold must be in [0, 1]")
        if max_missed < 0:
            raise ValueError("max_missed must be non-negative")
        self.iou_threshold = iou_threshold
        self.max_missed = max_missed
        self.tracks: list[Track] = []
        self._next_id = 1

    def update(self, detections: list[Detection]) -> list[Track]:
        """Advance one frame and return active tracks ordered by track ID.

        Match only detections and tracks with the same class. A match updates box
        and score, increments age/hits, and resets missed. An unmatched track ages
        and increments missed; delete it only when missed exceeds `max_missed`.
        An unmatched detection starts a new track. IDs are monotonic and never
        reused.
        """
        # LEARNER TODO: build a class-masked IoU matrix, associate, and apply lifecycle rules.
        raise NotImplementedError("implement IoUTracker.update")

