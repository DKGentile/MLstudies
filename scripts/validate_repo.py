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

    for chapter in manifest.get("chapters", []):
        path = ROOT / chapter["path"]
        if not path.is_dir():
            errors.append(f"missing chapter directory: {path.relative_to(ROOT)}")
        elif not (path / "README.md").is_file():
            errors.append(f"missing chapter README: {path.relative_to(ROOT) / 'README.md'}")

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
