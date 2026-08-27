from __future__ import annotations

import os

import numpy as np
import pytest

from computer_vision.conv_pool import (
    average_pool2d_nchw,
    conv2d_nchw,
    max_pool2d_nchw,
    output_size,
)


pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_CV_EXERCISES") != "1",
    reason="set RUN_CV_EXERCISES=1 to run learner challenges",
)


@pytest.mark.parametrize(
    ("input_size", "kernel_size", "stride", "padding", "expected"),
    [
        (5, 3, 1, 0, 3),
        (5, 3, 2, 0, 2),
        (5, 3, 2, 1, 3),
        (4, 4, 1, 0, 1),
    ],
)
def test_output_size_uses_floor_semantics(
    input_size: int,
    kernel_size: int,
    stride: int,
    padding: int,
    expected: int,
) -> None:
    assert output_size(input_size, kernel_size, stride=stride, padding=padding) == expected


@pytest.mark.parametrize(
    ("input_size", "kernel_size", "stride", "padding"),
    [(0, 1, 1, 0), (3, 4, 1, 0), (3, 1, 0, 0), (3, 1, 1, -1)],
)
def test_output_size_rejects_invalid_geometry(
    input_size: int,
    kernel_size: int,
    stride: int,
    padding: int,
) -> None:
    with pytest.raises(ValueError):
        output_size(input_size, kernel_size, stride=stride, padding=padding)


def test_one_by_one_convolution_is_an_identity_with_bias() -> None:
    inputs = np.arange(6.0).reshape(1, 1, 2, 3)
    original = inputs.copy()
    kernels = np.ones((1, 1, 1, 1))

    actual = conv2d_nchw(inputs, kernels, bias=np.array([0.25]))

    np.testing.assert_allclose(actual, inputs + 0.25)
    assert actual.dtype == np.float64
    np.testing.assert_array_equal(inputs, original)


def test_convolution_mixes_input_channels_into_each_output_channel() -> None:
    inputs = np.array(
        [
            [
                [[1.0, 2.0], [3.0, 4.0]],
                [[5.0, 6.0], [7.0, 8.0]],
            ]
        ]
    )
    kernels = np.array(
        [
            [[[1.0]], [[10.0]]],
            [[[-1.0]], [[0.5]]],
        ]
    )
    bias = np.array([0.0, 1.0])

    actual = conv2d_nchw(inputs, kernels, bias)

    expected_first = inputs[:, 0] + 10.0 * inputs[:, 1]
    expected_second = -inputs[:, 0] + 0.5 * inputs[:, 1] + 1.0
    expected = np.stack((expected_first, expected_second), axis=1)
    np.testing.assert_allclose(actual, expected)


def test_convolution_combines_stride_and_zero_padding() -> None:
    inputs = np.arange(1.0, 10.0).reshape(1, 1, 3, 3)
    kernels = np.ones((1, 1, 2, 2))

    actual = conv2d_nchw(inputs, kernels, stride=2, padding=1)

    np.testing.assert_allclose(actual, [[[[1.0, 5.0], [11.0, 28.0]]]])


def test_convolution_rejects_channel_mismatch() -> None:
    with pytest.raises(ValueError):
        conv2d_nchw(np.zeros((2, 3, 5, 5)), np.zeros((4, 2, 3, 3)))


def test_non_overlapping_max_pool() -> None:
    inputs = np.arange(1.0, 17.0).reshape(1, 1, 4, 4)

    actual = max_pool2d_nchw(inputs, kernel_size=2)

    np.testing.assert_allclose(actual, [[[[6.0, 8.0], [14.0, 16.0]]]])


def test_overlapping_max_pool_preserves_batch_and_channels() -> None:
    inputs = np.array(
        [
            [
                [[1.0, 9.0, 2.0], [3.0, 4.0, 8.0], [7.0, 6.0, 5.0]],
                [[-1.0, -2.0, -3.0], [-4.0, -5.0, -6.0], [-7.0, -8.0, -9.0]],
            ]
        ]
    )

    actual = max_pool2d_nchw(inputs, kernel_size=2, stride=1)

    expected = np.array(
        [
            [
                [[9.0, 9.0], [7.0, 8.0]],
                [[-1.0, -2.0], [-4.0, -5.0]],
            ]
        ]
    )
    np.testing.assert_allclose(actual, expected)


def test_average_pool_uses_all_values_in_each_window() -> None:
    inputs = np.arange(1.0, 17.0).reshape(1, 1, 4, 4)

    actual = average_pool2d_nchw(inputs, kernel_size=2)

    np.testing.assert_allclose(actual, [[[[3.5, 5.5], [11.5, 13.5]]]])


@pytest.mark.parametrize("function", [max_pool2d_nchw, average_pool2d_nchw])
def test_pooling_rejects_non_nchw_input(function) -> None:
    with pytest.raises(ValueError):
        function(np.zeros((3, 4, 4)), kernel_size=2)
