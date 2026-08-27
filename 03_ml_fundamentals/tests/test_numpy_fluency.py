from __future__ import annotations

import os

import numpy as np
import pytest

from ml_fundamentals.numpy_fluency import (
    gather_class_scores,
    rolling_windows,
    stable_softmax,
    standardize_columns,
)


pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_ML_EXERCISES") != "1",
    reason="set RUN_ML_EXERCISES=1 to run learner challenges",
)


def test_standardize_columns_handles_constant_column_without_mutation() -> None:
    x = np.array([[1.0, 2.0, 7.0], [3.0, 4.0, 7.0], [5.0, 6.0, 7.0]])
    original = x.copy()

    actual = standardize_columns(x)

    np.testing.assert_allclose(actual.mean(axis=0), np.zeros(3), atol=1e-12)
    np.testing.assert_allclose(actual[:, :2].std(axis=0), np.ones(2), atol=1e-12)
    np.testing.assert_array_equal(actual[:, 2], np.zeros(3))
    np.testing.assert_array_equal(x, original)


def test_standardize_columns_rejects_non_matrix() -> None:
    with pytest.raises(ValueError):
        standardize_columns(np.arange(5.0))


def test_gather_class_scores_uses_one_label_per_row() -> None:
    scores = np.array([[0.2, 4.0, -1.0], [2.5, 3.5, 8.0], [9.0, 1.0, 0.0]])
    labels = np.array([1, 2, 0])

    np.testing.assert_allclose(gather_class_scores(scores, labels), [4.0, 8.0, 9.0])


@pytest.mark.parametrize("labels", [np.array([0.0, 1.0]), np.array([0, 3])])
def test_gather_class_scores_rejects_invalid_labels(labels: np.ndarray) -> None:
    with pytest.raises((TypeError, ValueError, IndexError)):
        gather_class_scores(np.zeros((2, 3)), labels)


def test_stable_softmax_is_finite_normalized_and_shift_invariant() -> None:
    logits = np.array([[10_000.0, 10_001.0, 9_999.0], [-10_000.0, -10_002.0, -9_998.0]])

    probabilities = stable_softmax(logits)
    shifted = stable_softmax(logits + np.array([[123.0], [-456.0]]))

    assert np.isfinite(probabilities).all()
    np.testing.assert_allclose(probabilities.sum(axis=1), np.ones(2), atol=1e-12)
    np.testing.assert_allclose(probabilities, shifted, atol=1e-12)


def test_rolling_windows_returns_owned_rows() -> None:
    x = np.array([1.0, 2.0, 3.0, 4.0])
    windows = rolling_windows(x, 3)

    np.testing.assert_array_equal(windows, [[1.0, 2.0, 3.0], [2.0, 3.0, 4.0]])
    windows[0, 0] = 99.0
    assert x[0] == 1.0


@pytest.mark.parametrize("window_size", [0, -1, 5])
def test_rolling_windows_rejects_invalid_size(window_size: int) -> None:
    with pytest.raises(ValueError):
        rolling_windows(np.arange(4.0), window_size)
