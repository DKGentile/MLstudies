from __future__ import annotations

import pytest

from edge_course.tracker import Detection, IoUTracker


pytestmark = pytest.mark.exercise


def det(x1: float, y1: float, x2: float, y2: float, class_id: int = 0) -> Detection:
    return Detection((x1, y1, x2, y2), score=0.9, class_id=class_id)


def test_track_id_persists_for_overlapping_detection() -> None:
    tracker = IoUTracker(iou_threshold=0.3)
    first = tracker.update([det(0, 0, 10, 10)])
    second = tracker.update([det(1, 0, 11, 10)])
    assert [track.track_id for track in first] == [1]
    assert [track.track_id for track in second] == [1]
    assert second[0].hits == 2
    assert second[0].age == 2
    assert second[0].missed == 0


def test_track_survives_then_expires_after_missed_budget() -> None:
    tracker = IoUTracker(max_missed=1)
    tracker.update([det(0, 0, 1, 1)])
    assert [track.track_id for track in tracker.update([])] == [1]
    assert tracker.update([]) == []


def test_class_mismatch_creates_new_track() -> None:
    tracker = IoUTracker()
    tracker.update([det(0, 0, 10, 10, class_id=0)])
    tracks = tracker.update([det(0, 0, 10, 10, class_id=1)])
    assert [(track.track_id, track.class_id, track.missed) for track in tracks] == [
        (1, 0, 1),
        (2, 1, 0),
    ]


def test_ids_are_not_reused() -> None:
    tracker = IoUTracker(max_missed=0)
    tracker.update([det(0, 0, 1, 1)])
    tracker.update([])
    tracks = tracker.update([det(10, 10, 11, 11)])
    assert [track.track_id for track in tracks] == [2]

