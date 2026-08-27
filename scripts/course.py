"""Small, dependency-free navigator for the course manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "course_manifest.json"


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def list_chapters(data: dict) -> None:
    for chapter in data["chapters"]:
        print(
            f"{chapter['id']:<13} weeks {chapter['weeks']:<5} "
            f"{chapter['path']} -> {chapter['artifact']}"
        )


def show_week(data: dict, week: int) -> None:
    focus = data["week_focus"].get(str(week))
    if focus is None:
        raise SystemExit(f"week must be between 1 and {data['weeks']}")
    active = []
    for chapter in data["chapters"]:
        start, end = (int(value) for value in chapter["weeks"].split("-"))
        if start <= week <= end:
            active.append(chapter)
    print(f"Week {week}: {focus}")
    print("Active chapters:")
    for chapter in active:
        print(f"  - {chapter['path']}: {chapter['artifact']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="list all chapters")
    week_parser = subparsers.add_parser("week", help="show the focus for one week")
    week_parser.add_argument("number", type=int)
    args = parser.parse_args()
    data = load_manifest()
    if args.command == "list":
        list_chapters(data)
    else:
        show_week(data, args.number)


if __name__ == "__main__":
    main()

