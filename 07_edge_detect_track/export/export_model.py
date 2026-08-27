"""Export an Ultralytics checkpoint to ONNX with explicit, logged arguments."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--imgsz", type=int, default=416)
    parser.add_argument("--opset", type=int, default=17)
    parser.add_argument("--dynamic", action="store_true")
    parser.add_argument("--simplify", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.model.is_file():
        raise SystemExit(f"checkpoint not found: {args.model}")
    manifest = {
        "model": str(args.model),
        "model_sha256": sha256(args.model),
        "imgsz": args.imgsz,
        "opset": args.opset,
        "dynamic": args.dynamic,
        "simplify": args.simplify,
    }
    print(json.dumps(manifest, indent=2))
    if args.dry_run:
        return
    try:
        import ultralytics
        from ultralytics import YOLO
    except ImportError as exc:
        raise SystemExit("install requirements-deploy.txt in the active environment") from exc
    print(f"ultralytics={ultralytics.__version__}")
    output = YOLO(str(args.model)).export(
        format="onnx",
        imgsz=args.imgsz,
        opset=args.opset,
        dynamic=args.dynamic,
        simplify=args.simplify,
    )
    print(f"exported={output}")


if __name__ == "__main__":
    main()

