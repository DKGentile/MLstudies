# TensorRT C++ Inference Path

## Prepare

Read TensorRT's [inference-library documentation](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/),
[engine compatibility rules](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/engine-compatibility.html),
and [benchmarking guidance](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html).
For reduced precision, also read its [accuracy considerations](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/accuracy-considerations.html).

Before coding, draw ownership and lifetime for the engine, execution context,
stream, device buffers, pinned host buffers, and tensor shapes. Mark every
operation ordered by the stream and every host synchronization. The exact API
surface is version-specific; those invariants are not.

Build this only after Python/ONNX correctness is established. TensorRT APIs differ
substantially between the Nano's JetPack-provided version and a current desktop
release, so keep target adapters separate behind one small interface.

## Required components

1. RAII wrappers for CUDA buffers, streams, and TensorRT objects.
2. Engine deserialization with input/output tensor-name validation.
3. Pinned host buffers and asynchronous copies on one explicit stream.
4. Letterbox and box-restoration parity with the Python implementation.
5. Detection decode/NMS parity on a frozen test image.
6. Warmup, CUDA-event model timing, and end-to-end wall timing.
7. A machine-readable JSON or CSV benchmark output.

[main.cpp](main.cpp) is a CLI skeleton. Implement its `run_pipeline` boundary first;
then move TensorRT-version-specific code into `desktop/` or `nano/` rather than
filling `main` with conditional compilation.

## Build shape

```bash
cmake -S inference_cpp -B build/infer -DCMAKE_BUILD_TYPE=Release
cmake --build build/infer --config Release
```

The initial skeleton needs only C++17. Add OpenCV, CUDA, and TensorRT discovery when
the corresponding adapter is implemented. Pin include/library paths per machine in
the local build preset, not in committed source.

## Review questions

- Which allocations occur per frame, and how will you remove them?
- Where is synchronization necessary for correctness versus only for timing?
- Which TensorRT tensors are dynamic, and where are their shapes set?
- Who owns each pointer, and on which device/stream is it valid?
- Does postprocessing dominate after FP16 makes inference faster?
