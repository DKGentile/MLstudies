#!/usr/bin/env sh
set -eu

module_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
pattern=${1:-}

if ! command -v cmake >/dev/null 2>&1; then
  echo "CMake was not found. Read BUILDING.md and install CMake plus a C++17 compiler." >&2
  exit 2
fi

cd "$module_root"
cmake --preset default
cmake --build --preset default

if [ -n "$pattern" ]; then
  ctest --test-dir build -C Debug -R "$pattern" --output-on-failure
else
  ctest --preset default
fi

