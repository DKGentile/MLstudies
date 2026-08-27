"""Minimal YOLO-label auditor to extend during the capstone."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def validate_yolo_row(row: str, num_classes: int) -> tuple[int, float, float, float, float]:
    """Parse `class x_center y_center width height` or raise ValueError.

    Require exactly five finite fields, an integer class in range, centers and
    dimensions in [0, 1], and strictly positive width/height.
    """
    # LEARNER TODO: implement parsing and all invariants in the docstring.
    raise NotImplementedError("implement validate_yolo_row")


def audit_label_directory(labels: Path, num_classes: int) -> dict:
    report = {"files": 0, "boxes": 0, "empty_files": 0, "invalid": []}
    for path in sorted(labels.rglob("*.txt")):
        report["files"] += 1
        rows = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not rows:
            report["empty_files"] += 1
        for line_number, row in enumerate(rows, start=1):
            try:
                validate_yolo_row(row, num_classes)
                report["boxes"] += 1
            except ValueError as exc:
                report["invalid"].append(
                    {"file": str(path), "line": line_number, "reason": str(exc)}
                )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--labels", required=True, type=Path)
    parser.add_argument("--num-classes", required=True, type=int)
    args = parser.parse_args()
    if args.num_classes <= 0:
        raise SystemExit("--num-classes must be positive")
    if not args.labels.is_dir():
        raise SystemExit(f"label directory not found: {args.labels}")
    print(json.dumps(audit_label_directory(args.labels, args.num_classes), indent=2))


if __name__ == "__main__":
    main()

