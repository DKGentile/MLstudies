from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest


SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Keep a fresh scaffold green until capstone challenges are requested."""
    if os.environ.get("RUN_CAPSTONE_EXERCISES") == "1":
        return
    skip = pytest.mark.skip(reason="set RUN_CAPSTONE_EXERCISES=1 to run learner challenges")
    capstone_root = Path(__file__).resolve().parents[1]
    for item in items:
        item_path = Path(str(item.path)).resolve()
        if capstone_root in item_path.parents and item.get_closest_marker("exercise"):
            item.add_marker(skip)
