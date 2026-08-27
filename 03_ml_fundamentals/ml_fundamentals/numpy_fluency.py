"""Exercise 1: array manipulation used throughout the remaining labs."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def standardize_columns(x: ArrayLike) -> NDArray[np.float64]:
    """Return a standardized float copy of a two-dimensional feature matrix.

    Use population standard deviation (``ddof=0``). A constant column must
    become all zeros, and the input must not be mutated.
    """

    # TODO: validate the rank, then use reductions and broadcasting. Avoid a
    # Python loop over columns.
    raise NotImplementedError("implement standardize_columns")


def gather_class_scores(scores: ArrayLike, labels: ArrayLike) -> NDArray[np.float64]:
    """Select one class score per row using integer labels.

    ``scores`` has shape ``(batch, classes)`` and ``labels`` has shape
    ``(batch,)``. Reject non-integer labels and labels outside the class range.
    """

    # TODO: solve with NumPy advanced indexing rather than a Python loop.
    raise NotImplementedError("implement gather_class_scores")


def stable_softmax(logits: ArrayLike) -> NDArray[np.float64]:
    """Compute a row-wise softmax for a two-dimensional array of logits.

    The result must remain finite for very large-magnitude finite inputs. Do
    not mutate ``logits``.
    """

    # TODO: identify the per-row quantity that can be removed without changing
    # softmax probabilities, then normalize with broadcasting.
    raise NotImplementedError("implement stable_softmax")


def rolling_windows(x: ArrayLike, window_size: int) -> NDArray[np.float64]:
    """Return every contiguous 1-D window as rows of a new array.

    For an input of length ``n``, the output shape is
    ``(n - window_size + 1, window_size)``. Reject non-1-D input and invalid
    window sizes. The returned array must not share writable memory with the
    input.
    """

    # TODO: use NumPy's sliding-window facilities, then make the ownership
    # semantics in the docstring explicit.
    raise NotImplementedError("implement rolling_windows")
