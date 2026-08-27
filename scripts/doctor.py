"""Read-only capability report for the course machines."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


COMMANDS = ("git", "cmake", "ninja", "g++", "clang++", "cl", "nvcc", "nvidia-smi")
PACKAGES = ("numpy", "pytest", "torch", "torchvision", "cv2", "onnx", "onnxruntime")


def visual_studio_tools() -> dict[str, str]:
    """Find command-line tools bundled with Visual Studio Build Tools.

    MSVC is intentionally absent from a normal PowerShell PATH. Discovering it
    here distinguishes "not installed" from "open a Developer shell".
    """
    roots = [
        Path(r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools"),
        Path(r"C:\Program Files\Microsoft Visual Studio\2022\BuildTools"),
    ]
    for root in roots:
        if not root.is_dir():
            continue
        versions_root = root / "VC" / "Tools" / "MSVC"
        versions = sorted(
            (path for path in versions_root.glob("*") if path.is_dir()), reverse=True
        )
        compiler = versions[0] / "bin" / "Hostx64" / "x64" / "cl.exe" if versions else None
        candidates = {
            "cl": compiler,
            "cmake": root
            / "Common7"
            / "IDE"
            / "CommonExtensions"
            / "Microsoft"
            / "CMake"
            / "CMake"
            / "bin"
            / "cmake.exe",
            "ninja": root
            / "Common7"
            / "IDE"
            / "CommonExtensions"
            / "Microsoft"
            / "CMake"
            / "Ninja"
            / "ninja.exe",
            "developer_shell": root / "Common7" / "Tools" / "Launch-VsDevShell.ps1",
        }
        return {name: str(path) for name, path in candidates.items() if path and path.is_file()}
    return {}


VS_TOOLS = visual_studio_tools()


def tool_path(command: str) -> str | None:
    return shutil.which(command) or VS_TOOLS.get(command)


def first_line(command: str, *args: str) -> str | None:
    executable = tool_path(command)
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
    raw_output = (
        f"{result.stderr}\n{result.stdout}" if command == "cl" else (result.stdout or result.stderr)
    )
    output = raw_output.strip().splitlines()
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
    commands = {name: first_line(name, *command_args[name]) for name in COMMANDS}
    packages = {name: package_version(name) for name in PACKAGES}
    cpp_compiler = next((name for name in ("cl", "g++", "clang++") if commands[name]), None)
    report: dict[str, Any] = {
        "platform": platform.platform(),
        "python": sys.version.replace("\n", " "),
        "executable": sys.executable,
        "commands": commands,
        "command_paths": {name: tool_path(name) for name in COMMANDS},
        "packages": packages,
        "course_readiness": {
            "cpp": bool(cpp_compiler and commands["cmake"]),
            "cpp_compiler": cpp_compiler,
            "python_core": all(packages[name] for name in ("numpy", "pytest")),
            "cuda": bool(commands["nvcc"] and commands["nvidia-smi"]),
        },
    }
    if VS_TOOLS:
        report["visual_studio_build_tools"] = {
            "developer_shell": VS_TOOLS.get("developer_shell"),
            "note": "MSVC tools require a Visual Studio Developer shell in the terminal",
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
    readiness = report["course_readiness"]
    cpp_detail = f"ready via {readiness['cpp_compiler']}" if readiness["cpp"] else "not ready"
    print("\nCourse readiness")
    print(f"  C++ / systems  {cpp_detail}")
    print(f"  Python core    {'ready' if readiness['python_core'] else 'not ready'}")
    print(f"  CUDA labs      {'ready' if readiness['cuda'] else 'not ready on this machine'}")
    print("\nCommands")
    for name, value in report["commands"].items():
        print(f"  {name:<12} {value or 'missing'}")
        path = report["command_paths"].get(name)
        if path and not shutil.which(name):
            print(f"  {'':<12} installed at {path} (Developer shell required)")
    print("\nPython packages")
    for name, value in report["packages"].items():
        print(f"  {name:<12} {value or 'missing'}")
    runtime = report.get("torch_runtime")
    if runtime:
        print("\nPyTorch CUDA")
        for key, value in runtime.items():
            print(f"  {key:<15} {value}")
    visual_studio = report.get("visual_studio_build_tools")
    if visual_studio:
        print("\nVisual Studio Build Tools")
        print(f"  developer shell {visual_studio['developer_shell']}")
        print(f"  note            {visual_studio['note']}")
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
