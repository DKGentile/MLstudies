from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "dataset" / "audit_yolo.py"
SPEC = importlib.util.spec_from_file_location("audit_yolo", MODULE_PATH)
assert SPEC and SPEC.loader
audit_yolo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_yolo)

pytestmark = pytest.mark.exercise


def test_valid_row_is_parsed() -> None:
    assert audit_yolo.validate_yolo_row("2 0.5 0.25 0.1 1.0", 3) == (
        2,
        0.5,
        0.25,
        0.1,
        1.0,
    )


@pytest.mark.parametrize(
    "row,num_classes",
    [
        ("0 0.5 0.5 0.2", 1),
        ("1 0.5 0.5 0.2 0.2", 1),
        ("0.5 0.5 0.5 0.2 0.2", 2),
        ("0 nan 0.5 0.2 0.2", 1),
        ("0 1.1 0.5 0.2 0.2", 1),
        ("0 0.5 0.5 0 0.2", 1),
    ],
)
def test_invalid_rows_are_rejected(row: str, num_classes: int) -> None:
    with pytest.raises(ValueError):
        audit_yolo.validate_yolo_row(row, num_classes)

