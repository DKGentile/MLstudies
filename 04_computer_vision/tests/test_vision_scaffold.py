from __future__ import annotations

from computer_vision import conv_pool


def test_vision_primitive_module_imports() -> None:
    assert callable(conv_pool.output_size)
    assert callable(conv_pool.conv2d_nchw)
    assert callable(conv_pool.max_pool2d_nchw)
    assert callable(conv_pool.average_pool2d_nchw)
