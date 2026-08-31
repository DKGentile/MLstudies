"""Print a dated 26-week schedule from a Monday start date."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_date(value: str) -> dt.date:
    try:
        result = dt.date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("use YYYY-MM-DD") from exc
    if result.weekday() != 0:
        raise argparse.ArgumentTypeError(f"{value} is not a Monday")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", required=True, type=parse_date)
    args = parser.parse_args()
    manifest = json.loads((ROOT / "course_manifest.json").read_text(encoding="utf-8"))
    tracks = manifest.get("application_tracks", {})
    if tracks:
        print("> Application timing is evidence-based, not a 26-week embargo:")
        for name in ("A", "B", "C"):
            if name in tracks:
                print(f"> - Track {name}: {tracks[name]}")
        print(">")
    print("| Week | Starts | Focus |")
    print("|---:|---|---|")
    for week in range(1, manifest["weeks"] + 1):
        date = args.start + dt.timedelta(weeks=week - 1)
        print(f"| {week} | {date.isoformat()} | {manifest['week_focus'][str(week)]} |")


if __name__ == "__main__":
    main()
