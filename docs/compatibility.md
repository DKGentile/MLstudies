# Hardware and Version Strategy

Last reviewed: **2026-08-30**. Re-check the linked support matrices before changing
a working machine.

## Keep three environments separate

| Machine | Course job | Key constraint |
|---|---|---|
| RTX 5060 Ti host | Training, current CUDA, current TensorRT, profiling | Use a current driver/toolkit combination and build engines locally |
| GTX 1080 | CUDA fundamentals and cross-architecture comparison | Pascal (SM 6.1) is not supported by current TensorRT releases; use a compatible archived stack only if TensorRT is truly needed |
| Original Jetson Nano | Final tiny-model deployment | Remains on the JetPack 4.6.x / L4T 32.x generation; modern desktop wheels and engines do not transfer |

TensorRT plan/engine files are not portable binaries. Preserve the ONNX model and
the engine-build command, then build on the target. Even hardware-compatibility
modes have platform limitations.

## Model naming

Ultralytics' current examples may use a newer nano model name than older Jetson
guides. The capstone therefore takes `--model` as a parameter and never makes the
model filename part of the architecture. For an original Nano, start with a small,
known-exportable model and a 320 or 416 pixel input. Record the exact weight hash,
package version, opset, and export flags.

## Python and PyTorch

Use PyTorch's official installer selector for the host CUDA wheel. A Python 3.12
environment remains a conservative interoperability choice when ONNX, TensorRT,
OpenCV, and training packages must coexist. The Jetson uses the Python and binary
packages compatible with its JetPack image, not the host environment.

## Native diagnostics and networking

| Capability | Native Windows/MSVC | Linux or WSL GCC/Clang |
|---|---|---|
| Debugger | Visual Studio/VS Code debugger | GDB or LLDB |
| AddressSanitizer | Supported on documented x86/x64 configurations | Supported when the compiler runtime is installed |
| UndefinedBehaviorSanitizer | Not supplied by MSVC | Use the course ASan+UBSan configuration |
| ThreadSanitizer | Not supplied by MSVC; do not imply native support | Separate TSan build; never combine with ASan |
| TCP lab | Winsock loopback, linked from the Windows SDK | POSIX loopback sockets |
| Socket observation | platform network tools are optional | `ss`; optional privileged `tcpdump`; optional `strace` |

The intentional bug clinics are opt-in, separate build trees and are never normal
CTest failures. Sanitizer support belongs to a compiler **and** its installed
runtime; a `clang++` found on `PATH` is not sufficient evidence by itself.

TCP tests use only `127.0.0.1`, ephemeral ports, and deterministic local payloads.
No external service or internet access is part of their correctness contract.

## Camera geometry dependency boundary

The required geometry implementation is NumPy-only. OpenCV may be used after the
first attempt as an independent projection/calibration oracle, but is not required
just to complete the lab. The course covers calibration and radial/tangential
distortion conceptually without adding stereo, reconstruction, visual odometry,
bundle adjustment, or SLAM.

## Primary references

- [PyTorch local installation](https://pytorch.org/get-started/locally/)
- [NVIDIA TensorRT support matrix](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html)
- [TensorRT engine compatibility](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/engine-compatibility.html)
- [NVIDIA JetPack archive](https://developer.nvidia.com/embedded/jetpack-archive)
- [Ultralytics train mode](https://docs.ultralytics.com/modes/train/)
- [Ultralytics export mode](https://docs.ultralytics.com/modes/export/)
- [Ultralytics track mode](https://docs.ultralytics.com/modes/track/)
- [MSVC AddressSanitizer](https://learn.microsoft.com/en-us/cpp/sanitizers/asan?view=msvc-170)
- [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html),
  [UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html),
  and [ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html)
