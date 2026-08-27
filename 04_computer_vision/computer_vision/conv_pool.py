"""NumPy exercises for convolution and pooling in NCHW layout."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def output_size(
    input_size: int,
    kernel_size: int,
    *,
    stride: int = 1,
    padding: int = 0,
) -> int:
    """Return one spatial output dimension using floor semantics.

    Reject non-positive input/kernel/stride, negative padding, and a kernel
    whose padded effective input is too small.
    """

    # TODO: translate the convolution output-size equation into integer
    # arithmetic and validate its domain.
    raise NotImplementedError("implement output_size")


def conv2d_nchw(
    inputs: ArrayLike,
    kernels: ArrayLike,
    bias: ArrayLike | None = None,
    *,
    stride: int = 1,
    padding: int = 0,
) -> NDArray[np.float64]:
    """Apply multi-channel 2-D cross-correlation to an NCHW batch.

    ``inputs`` has shape ``(N, C_in, H, W)`` and ``kernels`` has shape
    ``(C_out, C_in, K_h, K_w)``. ``bias`` is absent or has shape ``(C_out,)``.
    Return a newly allocated float64 array. Padding is symmetric and filled
    with zeros; stride applies to both spatial dimensions.
    """

    # TODO: validate ranks/channels/bias, determine the two output dimensions,
    # pad once, and accumulate each receptive-field dot product. Start with a
    # readable reference implementation; vectorization is optional.
    raise NotImplementedError("implement conv2d_nchw")


def max_pool2d_nchw(
    inputs: ArrayLike,
    *,
    kernel_size: int,
    stride: int | None = None,
) -> NDArray[np.float64]:
    """Apply square max pooling without padding to an NCHW batch.

    A missing stride means non-overlapping pooling (``stride=kernel_size``).
    Return float64 output and never mutate the input.
    """

    # TODO: preserve batch/channel axes and reduce only each spatial window.
    raise NotImplementedError("implement max_pool2d_nchw")


def average_pool2d_nchw(
    inputs: ArrayLike,
    *,
    kernel_size: int,
    stride: int | None = None,
) -> NDArray[np.float64]:
    """Apply square average pooling without padding to an NCHW batch.

    A missing stride means ``stride=kernel_size``. Use the ordinary arithmetic
    mean over every complete spatial window.
    """

    # TODO: mirror max_pool2d_nchw's validation and traversal, changing only
    # the reduction performed for each window.
    raise NotImplementedError("implement average_pool2d_nchw")
