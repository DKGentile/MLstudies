#!/usr/bin/env sh
set -eu

module_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
pattern=${1:-}

if ! command -v cmake >/dev/null 2>&1; then
  echo "CMake was not found. Install CMake and a C++17 compiler first." >&2
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
