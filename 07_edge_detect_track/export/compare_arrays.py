"""Compare saved reference and exported-runtime tensors without hiding tolerances."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def comparison(reference: np.ndarray, candidate: np.ndarray) -> dict:
    if reference.shape != candidate.shape:
        return {"same_shape": False, "reference_shape": reference.shape, "candidate_shape": candidate.shape}
    absolute = np.abs(reference.astype(np.float64) - candidate.astype(np.float64))
    denominator = np.maximum(np.abs(reference.astype(np.float64)), 1e-12)
    relative = absolute / denominator
    return {
        "same_shape": True,
        "elements": int(reference.size),
        "max_abs": float(absolute.max(initial=0.0)),
        "mean_abs": float(absolute.mean()) if absolute.size else 0.0,
        "max_rel": float(relative.max(initial=0.0)),
        "all_finite": bool(np.isfinite(candidate).all()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--atol", type=float, required=True)
    parser.add_argument("--rtol", type=float, required=True)
    args = parser.parse_args()
    reference = np.load(args.reference)
    candidate = np.load(args.candidate)
    report = comparison(reference, candidate)
    report["within_tolerance"] = bool(
        report.get("same_shape")
        and np.allclose(reference, candidate, atol=args.atol, rtol=args.rtol)
    )
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["within_tolerance"] else 1)


if __name__ == "__main__":
    main()

