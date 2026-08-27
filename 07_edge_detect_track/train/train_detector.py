"""Thin, explicit Ultralytics training entry point for reproducible experiments."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_if_file(value: str) -> str | None:
    path = Path(value)
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--imgsz", type=int, default=416)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--device", default="0")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--project", default="runs/edge-detect-track")
    parser.add_argument("--name", required=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = vars(args) | {"model_sha256": sha256_if_file(args.model)}
    print(json.dumps(manifest, indent=2))
    if args.dry_run:
        return
    try:
        import ultralytics
        from ultralytics import YOLO
    except ImportError as exc:
        raise SystemExit("install requirements-deploy.txt in the active environment") from exc
    print(f"ultralytics={ultralytics.__version__}")
    model = YOLO(args.model)
    model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        workers=args.workers,
        seed=args.seed,
        deterministic=True,
        project=args.project,
        name=args.name,
    )


if __name__ == "__main__":
    main()

