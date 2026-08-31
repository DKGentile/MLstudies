"""Validate the unsolved course scaffold without running learner exercises."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import re
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "build",
    "__pycache__",
}
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
EXPECTED_WEEKS = 26
EXPECTED_CHAPTER_RANGES = {
    "cpp": "1-4",
    "systems": "1-4",
    "ml": "3-6",
    "cv": "5-9",
    "cuda": "6-12",
    "optimization": "11-14",
    "capstone": "10-22",
    "interviews": "18-26",
}
REQUIRED_HARDENING_PATHS = (
    "01_cpp_fluency/modern_cpp_engineering/README.md",
    "01_cpp_fluency/modern_cpp_engineering/EXERCISES.md",
    "01_cpp_fluency/modern_cpp_engineering/include/owned_buffer.hpp",
    "01_cpp_fluency/modern_cpp_engineering/starter/owned_buffer.cpp",
    "01_cpp_fluency/modern_cpp_engineering/tests/owned_buffer_tests.cpp",
    "01_cpp_fluency/debugging_clinics/README.md",
    "01_cpp_fluency/debugging_clinics/lifetime_bug.cpp",
    "01_cpp_fluency/debugging_clinics/bounds_bug.cpp",
    "02_systems/week03_threads_locks/debugging/racy_metrics.cpp",
    "02_systems/week04_integration/README.md",
    "02_systems/week04_integration/include/frame_protocol.hpp",
    "02_systems/week04_integration/include/tcp_pipeline.hpp",
    "02_systems/week04_integration/include/tcp_socket.hpp",
    "02_systems/week04_integration/infrastructure/tcp_socket.cpp",
    "02_systems/week04_integration/starter/frame_protocol.cpp",
    "02_systems/week04_integration/starter/tcp_pipeline.cpp",
    "02_systems/week04_integration/tests/frame_protocol_tests.cpp",
    "02_systems/week04_integration/tests/tcp_pipeline_tests.cpp",
    "02_systems/week04_integration/tests/tcp_socket_tests.cpp",
    "02_systems/week04_integration/probe/fake_sensor.cpp",
    "02_systems/week04_integration/probe/tcp_receiver.cpp",
    "04_computer_vision/computer_vision/camera_geometry.py",
    "04_computer_vision/tests/test_camera_geometry.py",
    "08_interviews/interview_recon.md",
    "08_interviews/interview_recon.template.md",
)


def iter_python_files():
    for path in ROOT.rglob("*.py"):
        if not SKIP_PARTS.intersection(path.parts):
            yield path


def main() -> None:
    errors: list[str] = []
    manifest_path = ROOT / "course_manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"manifest error: {exc}")

    if manifest.get("weeks") != EXPECTED_WEEKS:
        errors.append(
            f"course must remain exactly {EXPECTED_WEEKS} weeks; "
            f"found {manifest.get('weeks')!r}"
        )

    expected_week_keys = {str(week) for week in range(1, EXPECTED_WEEKS + 1)}
    actual_week_keys = set(manifest.get("week_focus", {}))
    if actual_week_keys != expected_week_keys:
        missing = sorted(expected_week_keys - actual_week_keys, key=int)
        extra = sorted(actual_week_keys - expected_week_keys)
        errors.append(f"manifest week_focus mismatch: missing={missing}, extra={extra}")

    application_tracks = manifest.get("application_tracks", {})
    if set(application_tracks) != {"A", "B", "C"} or not all(
        isinstance(description, str) and description.strip()
        for description in application_tracks.values()
    ):
        errors.append(
            "manifest application_tracks must define nonempty Track A, B, and C"
        )

    chapter_ranges = {
        chapter.get("id"): chapter.get("weeks")
        for chapter in manifest.get("chapters", [])
    }
    if chapter_ranges != EXPECTED_CHAPTER_RANGES:
        errors.append(
            "manifest chapter ranges differ from the frozen curriculum: "
            f"expected={EXPECTED_CHAPTER_RANGES}, found={chapter_ranges}"
        )

    for relative in REQUIRED_HARDENING_PATHS:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required curriculum-hardening file: {relative}")

    course_map_text = (ROOT / "COURSE_MAP.md").read_text(encoding="utf-8")
    course_map_weeks = [
        int(match)
        for match in re.findall(r"^\|\s*(\d+)\s*\|", course_map_text, re.MULTILINE)
    ]
    if course_map_weeks != list(range(1, EXPECTED_WEEKS + 1)):
        errors.append(
            "COURSE_MAP numbered rows must contain each week exactly from 1 to "
            f"{EXPECTED_WEEKS}; found={course_map_weeks}"
        )

    for chapter in manifest.get("chapters", []):
        path = ROOT / chapter["path"]
        if not path.is_dir():
            errors.append(f"missing chapter directory: {path.relative_to(ROOT)}")
        elif not (path / "README.md").is_file():
            errors.append(f"missing chapter README: {path.relative_to(ROOT) / 'README.md'}")
        try:
            start, end = (int(value) for value in chapter["weeks"].split("-"))
        except (KeyError, AttributeError, ValueError):
            errors.append(f"invalid chapter week range: {chapter!r}")
        else:
            if not (1 <= start <= end <= EXPECTED_WEEKS):
                errors.append(
                    f"chapter range outside 1..{EXPECTED_WEEKS}: "
                    f"{chapter.get('id', chapter.get('path'))}={chapter['weeks']}"
                )

    checked_links = 0
    for markdown in ROOT.rglob("*.md"):
        if SKIP_PARTS.intersection(markdown.parts):
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            # Ignore an optional Markdown title and an in-page fragment.
            target = target.split(' "', 1)[0].split("#", 1)[0]
            if not target:
                continue
            checked_links += 1
            resolved = (markdown.parent / unquote(target)).resolve()
            if not resolved.exists():
                errors.append(
                    f"broken local link in {markdown.relative_to(ROOT)}: {raw_target}"
                )

    parsed = 0
    for path in iter_python_files():
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            parsed += 1
        except (OSError, SyntaxError, UnicodeError) as exc:
            errors.append(f"Python parse failure in {path.relative_to(ROOT)}: {exc}")

    todo_count = 0
    for suffix in ("*.py", "*.cpp", "*.cu", "*.hpp"):
        for path in ROOT.rglob(suffix):
            if SKIP_PARTS.intersection(path.parts):
                continue
            try:
                todo_count += path.read_text(encoding="utf-8").count("LEARNER TODO")
            except UnicodeDecodeError:
                errors.append(f"non-UTF-8 source file: {path.relative_to(ROOT)}")

    if todo_count < 10:
        errors.append(f"expected at least 10 learner exercises; found {todo_count}")

    application_guidance = "\n".join(
        (ROOT / relative).read_text(encoding="utf-8").lower()
        for relative in (
            "README.md",
            "COURSE_MAP.md",
            "course_manifest.json",
            "docs/curriculum_mapping.md",
            "08_interviews/README.md",
        )
    )
    for stale_phrase in (
        "applications begin",
        "start applications",
        "applications begin when gates pass",
        "start applications when the capstone",
        "when the capstone contains",
    ):
        if stale_phrase in application_guidance:
            errors.append(f"stale application-embargo guidance remains: {stale_phrase!r}")

    if errors:
        print("Course validation failed:")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)
    print(
        f"Course scaffold OK: {len(manifest['chapters'])} chapters, "
        f"{parsed} Python files parsed, {checked_links} local links checked, "
        f"{todo_count} learner TODOs."
    )


if __name__ == "__main__":
    main()
