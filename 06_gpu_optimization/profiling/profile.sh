#!/usr/bin/env bash
set -u

usage() {
  echo "Usage: $0 <ncu|nsys> <executable> <output-name> [program arguments...]"
  echo "Optional: KERNEL_FILTER='regex:kernel_name' for ncu (default regex:.*)."
  echo "Optional: LAUNCH_SKIP=N for ncu (default 0; counts matching kernels)."
}

if [ "$#" -lt 3 ]; then
  usage
  exit 2
fi

tool=$1
executable=$2
output_name=$3
shift 3

if [ "$tool" != "ncu" ] && [ "$tool" != "nsys" ]; then
  usage
  exit 2
fi

if ! command -v "$tool" >/dev/null 2>&1; then
  echo "$tool is not installed or not on PATH; profiling was skipped." >&2
  exit 0
fi

if [ ! -f "$executable" ] || [ ! -x "$executable" ]; then
  echo "Executable not found or not executable: $executable" >&2
  exit 2
fi

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
output_directory="$script_directory/../profiles"
mkdir -p -- "$output_directory"
output_base="$output_directory/$output_name"

echo "Profiler: $(command -v "$tool")"
echo "Executable: $executable"
echo "Output base: $output_base"

if [ "$tool" = "ncu" ]; then
  kernel_filter=${KERNEL_FILTER:-regex:.*}
  launch_skip=${LAUNCH_SKIP:-0}
  case $launch_skip in
    ''|*[!0-9]*)
      echo "LAUNCH_SKIP must be a non-negative integer." >&2
      exit 2
      ;;
  esac
  exec ncu \
    --set full \
    --target-processes all \
    --kernel-name-base function \
    --kernel-name "$kernel_filter" \
    --launch-skip "$launch_skip" \
    --launch-count 1 \
    --force-overwrite \
    --export "$output_base" \
    "$executable" "$@"
fi

exec nsys profile \
  --stats true \
  --force-overwrite true \
  --output "$output_base" \
  "$executable" "$@"
