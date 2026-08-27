from __future__ import annotations

import numpy as np
import pytest

from edge_course.geometry import box_iou_matrix


pytestmark = pytest.mark.exercise


def test_identity_disjoint_and_partial_overlap() -> None:
    a = np.array([[0, 0, 2, 2], [10, 10, 11, 11]], dtype=float)
    b = np.array([[0, 0, 2, 2], [1, 1, 3, 3]], dtype=float)
    actual = box_iou_matrix(a, b)
    np.testing.assert_allclose(actual, [[1.0, 1.0 / 7.0], [0.0, 0.0]])


def test_empty_inputs_keep_matrix_shape() -> None:
    actual = box_iou_matrix(np.empty((0, 4)), np.ones((3, 4)))
    assert actual.shape == (0, 3)


def test_degenerate_boxes_return_finite_zero() -> None:
    actual = box_iou_matrix(np.array([[1, 1, 1, 1.0]]), np.array([[1, 1, 1, 1.0]]))
    assert np.isfinite(actual).all()
    assert actual[0, 0] == 0.0


@pytest.mark.parametrize(
    "bad",
    [np.ones((4,)), np.ones((2, 5)), np.array([[2.0, 0.0, 1.0, 1.0]])],
)
def test_rejects_malformed_boxes(bad: np.ndarray) -> None:
    with pytest.raises(ValueError):
        box_iou_matrix(bad, np.ones((1, 4)))

