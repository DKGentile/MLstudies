from __future__ import annotations

import numpy as np
import pytest

from edge_course.matching import greedy_iou_match


pytestmark = pytest.mark.exercise


def test_greedy_choice_can_leave_a_lower_score_pair_unmatched() -> None:
    matrix = np.array([[0.9, 0.8], [0.7, 0.1]])
    matches, unmatched_rows, unmatched_cols = greedy_iou_match(matrix, threshold=0.2)
    # Greedy takes 0.9 first; the only remaining pair is below threshold. A
    # globally optimal assignment would take 0.8 and 0.7 instead. Preserve this
    # counterexample for the later Hungarian-assignment comparison.
    assert matches == [(0, 0)]
    assert unmatched_rows == [1]
    assert unmatched_cols == [1]


def test_threshold_and_unmatched_indices() -> None:
    matrix = np.array([[0.29, 0.1], [0.0, 0.8], [0.2, 0.1]])
    matches, unmatched_rows, unmatched_cols = greedy_iou_match(matrix, threshold=0.3)
    assert matches == [(1, 1)]
    assert unmatched_rows == [0, 2]
    assert unmatched_cols == [0]


def test_tie_break_is_deterministic() -> None:
    matches, _, _ = greedy_iou_match(np.full((2, 2), 0.5), threshold=0.5)
    assert matches == [(0, 0), (1, 1)]


def test_empty_matrix() -> None:
    assert greedy_iou_match(np.empty((0, 3)), 0.5) == ([], [], [0, 1, 2])
