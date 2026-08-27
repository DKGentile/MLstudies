# Original Jetson Nano Deployment

This lab targets the original Nano generation, not an Orin Nano. Treat it as a
legacy deployment target with its own immutable environment.

## Before touching the image

1. Boot the known-working SD card and capture [NOTES.template.md](NOTES.template.md).
2. Export or back up anything irreplaceable.
3. Confirm the exact JetPack/L4T release, power mode, storage, swap, free memory,
   and cooling.
4. Freeze a working image before upgrading individual packages.

## Port sequence

1. Copy the tested ONNX model and frozen parity inputs to the Nano.
2. Inspect the installed TensorRT parser/opset support.
3. Build the engine **on the Nano** at batch 1 and fixed input size.
4. Validate one frozen input against desktop ONNX outputs.
5. Benchmark inference-only, then the complete video pipeline.
6. Try FP16 only after FP32 correctness; try INT8 only if calibration quality can
   be evaluated honestly.

Start at 416 or 320 if 640 exhausts memory. The lower input size is an experiment:
report its accuracy cost alongside its latency and memory benefit.

## Time-box

Stop after one weekend if OS imaging, unsupported operators, or package conflicts
prevent model execution. Complete [DEFERRAL.template.md](DEFERRAL.template.md), keep
the measured desktop deployment, and return only if a narrower hypothesis emerges.

Official source of truth: [NVIDIA JetPack archive](https://developer.nvidia.com/embedded/jetpack-archive).

