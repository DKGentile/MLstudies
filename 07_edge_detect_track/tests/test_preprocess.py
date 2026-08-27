from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "inference_python" / "preprocess.py"
SPEC = importlib.util.spec_from_file_location("preprocess", MODULE_PATH)
assert SPEC and SPEC.loader
preprocess = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preprocess)

pytestmark = pytest.mark.exercise


def test_letterbox_shape_scale_and_fill() -> None:
    image = np.full((2, 4, 3), 7, dtype=np.uint8)
    canvas, scale, padding = preprocess.letterbox(image, 6, 6, fill=114)
    assert canvas.shape == (6, 6, 3)
    assert scale == pytest.approx(1.5)
    assert padding == (0, 1)
    assert np.all(canvas[0] == 114)
    assert np.all(canvas[1:4] == 7)
    assert np.all(canvas[4:] == 114)


def test_scale_boxes_back_undoes_transform_and_clips() -> None:
    transformed = np.array([[-1.0, 1.0, 7.0, 4.0], [1.5, 2.5, 4.5, 4.0]])
    actual = preprocess.scale_boxes_back(transformed, 1.5, (0, 1), 2, 4)
    np.testing.assert_allclose(actual, [[0, 0, 4, 2], [1, 1, 3, 2]])

