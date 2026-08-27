# Chapter 07 — Edge Detect + Track

**Weeks:** 10–22  
**Outcome:** a small, measured object detector and tracker with ONNX/TensorRT and a
time-boxed original Jetson Nano deployment.

This chapter is the portfolio project. The framework commands are deliberately
thin; your engineering work is dataset discipline, evaluation, tracking logic,
parity checks, profiling, and honest reporting.

## Architecture

```text
video/image
    │
    ▼
decode → resize/normalize → detector → confidence/NMS → detections
                                                       │
                                                       ▼
                                      IoU association → track lifecycle
                                                       │
                                                       ▼
                                              overlay / metrics / output
```

Measure decode, preprocess, inference, postprocess, tracking, and rendering
separately. “Model FPS” and “camera-to-output FPS” answer different questions.

## Milestones and gates

| Week | Required work | Evidence gate |
|---:|---|---|
| 10 | Write `PROJECT_SPEC.md`; audit a small public dataset | Scope, license, class counts, split policy |
| 12 | Train a small baseline | Config, curves, package versions, checkpoint hash |
| 14 | Evaluate and collect false positives/negatives | mAP/precision/recall plus failure examples |
| 16 | Export ONNX and compare outputs | Shapes and numeric/parity tolerance documented |
| 17 | Complete IoU, matching, and tracker exercises | Synthetic sequence tests pass |
| 18 | Run detection + tracking on a video | Demo plus stage-level latency breakdown |
| 20 | Build TensorRT on the RTX host | FP32/FP16 latency, memory, accuracy delta |
| 21 | Spend at most one weekend on the original Nano | Working result or explicit deferral report |
| 22 | Freeze the project | Reproduction steps work from a clean environment |

## Work in this order

1. [project brief](PROJECT_SPEC.md)
2. [dataset audit](dataset/README.md)
3. [detector training](train/README.md)
4. [detection metrics](src/edge_course/metrics.py)
5. [ONNX export and parity](export/README.md)
6. [IoU and matching](src/edge_course/geometry.py),
   [tracker lifecycle](src/edge_course/tracker.py), then the
   [tracking extensions](tracking/README.md)
7. [Python pipeline](inference_python/README.md)
8. [TensorRT/C++ path](inference_cpp/README.md)
9. [Jetson port](nano/README.md)
10. [results and failure analysis](results/README.md)

## Exercise tests

From this directory:

```powershell
$env:RUN_CAPSTONE_EXERCISES = "1"
python -m pytest tests -q
```

On bash/zsh, prefix the command with `RUN_CAPSTONE_EXERCISES=1`. Without this
explicit opt-in, pytest collects but skips the learner challenges so a fresh clone
can distinguish a healthy scaffold from unfinished work. The enabled tests are
intentionally red until the `LEARNER TODO` implementations are complete. Solve in
this order:

```powershell
python -m pytest tests/test_geometry.py -q
python -m pytest tests/test_metrics.py -q
python -m pytest tests/test_matching.py -q
python -m pytest tests/test_tracker.py -q
python -m pytest tests/test_kalman.py -q
```

## Scope guardrails

- Begin with 1–3 classes and a small model. Dataset quality matters more than a
  larger backbone.
- Implement a simple IoU tracker before adding Kalman filtering or ByteTrack.
- Build TensorRT engines on each target; do not copy a desktop engine to Jetson.
- At input 640, if the Nano path is unstable or out of memory, try 416 or 320 and
  record the accuracy/latency tradeoff.
- Do not spend more than one weekend repairing the legacy Nano image. A measured
  desktop TensorRT result remains a valid completed capstone.

The finished root README should lead with numbers, then architecture, then failure
analysis. Avoid claims that the benchmark setup does not support.
