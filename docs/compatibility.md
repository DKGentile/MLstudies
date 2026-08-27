# Hardware and Version Strategy

Last reviewed: **2026-08-27**. Re-check the linked support matrices before changing
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

## Primary references

- [PyTorch local installation](https://pytorch.org/get-started/locally/)
- [NVIDIA TensorRT support matrix](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html)
- [TensorRT engine compatibility](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/engine-compatibility.html)
- [NVIDIA JetPack archive](https://developer.nvidia.com/embedded/jetpack-archive)
- [Ultralytics train mode](https://docs.ultralytics.com/modes/train/)
- [Ultralytics export mode](https://docs.ultralytics.com/modes/export/)
- [Ultralytics track mode](https://docs.ultralytics.com/modes/track/)

