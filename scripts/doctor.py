"""Read-only capability report for the course machines."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import shutil
import subprocess
import sys
from typing import Any


COMMANDS = ("git", "cmake", "ninja", "g++", "clang++", "cl", "nvcc", "nvidia-smi")
PACKAGES = ("numpy", "pytest", "torch", "torchvision", "cv2", "onnx", "onnxruntime")


def first_line(command: str, *args: str) -> str | None:
    executable = shutil.which(command)
    if not executable:
        return None
    try:
        result = subprocess.run(
            [executable, *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=8,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "present (version probe failed)"
    output = (result.stdout or result.stderr).strip().splitlines()
    return output[0] if output else "present"


def package_version(name: str) -> str | None:
    if importlib.util.find_spec(name) is None:
        return None
    try:
        module = __import__(name)
        return str(getattr(module, "__version__", "present"))
    except Exception as exc:  # A broken binary package is useful diagnostic evidence.
        return f"import failed: {type(exc).__name__}: {exc}"


def collect() -> dict[str, Any]:
    command_args = {
        "git": ("--version",),
        "cmake": ("--version",),
        "ninja": ("--version",),
        "g++": ("--version",),
        "clang++": ("--version",),
        "cl": (),
        "nvcc": ("--version",),
        "nvidia-smi": ("--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"),
    }
    report: dict[str, Any] = {
        "platform": platform.platform(),
        "python": sys.version.replace("\n", " "),
        "executable": sys.executable,
        "commands": {name: first_line(name, *command_args[name]) for name in COMMANDS},
        "packages": {name: package_version(name) for name in PACKAGES},
    }
    try:
        import torch

        report["torch_runtime"] = {
            "cuda_build": torch.version.cuda,
            "cuda_available": torch.cuda.is_available(),
            "device_count": torch.cuda.device_count(),
        }
    except Exception:
        report["torch_runtime"] = None
    return report


def print_human(report: dict[str, Any]) -> None:
    print(f"Platform: {report['platform']}")
    print(f"Python:   {report['python']}")
    print("\nCommands")
    for name, value in report["commands"].items():
        print(f"  {name:<12} {value or 'missing'}")
    print("\nPython packages")
    for name, value in report["packages"].items():
        print(f"  {name:<12} {value or 'missing'}")
    runtime = report.get("torch_runtime")
    if runtime:
        print("\nPyTorch CUDA")
        for key, value in runtime.items():
            print(f"  {key:<15} {value}")
    print("\nMissing optional tools are expected until their chapter.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()
    report = collect()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human(report)


if __name__ == "__main__":
    main()

