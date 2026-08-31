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

Chapter 04's camera geometry and this capstone's box geometry answer different
questions. Intrinsics and extrinsics map a 3-D world or camera point to a pixel;
letterboxing maps between two 2-D image coordinate systems; IoU compares regions
already expressed in one image coordinate system. Name the relevant frames and
transforms instead of treating all three operations as interchangeable geometry.

Measure decode, preprocess, inference, postprocess, tracking, and rendering
separately. “Model FPS” and “camera-to-output FPS” answer different questions.

## Prepare by milestone

These are assigned sources, not a background bibliography. Read the core item
before the named work; use papers marked "after baseline" only once your simpler
implementation has exposed the failure they address.

| Week | Core source | What it prepares you to produce |
|---:|---|---|
| 10 | [Datasheets for Datasets](https://arxiv.org/abs/1803.09010), Ultralytics [detection dataset format](https://docs.ultralytics.com/datasets/detect), and scikit-learn [`GroupShuffleSplit`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html) | Provenance/license record, valid labels, and a split whose unit of independence is explicit |
| 11 | Ultralytics [training mode](https://docs.ultralytics.com/modes/train/) and PyTorch [reproducibility](https://docs.pytorch.org/docs/stable/notes/randomness.html) | Versioned baseline configuration with honest limits on reproducibility |
| 12 | PyTorch [transfer-learning tutorial](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html) | Tiny-subset overfit check and first controlled training run |
| 13 | Ultralytics [validation mode](https://docs.ultralytics.com/modes/val/) and COCO's [detection evaluation page](https://cocodataset.org/#detection-eval) | Per-class metrics with named IoU and score rules |
| 14 | The original [TIDE error-analysis paper](https://arxiv.org/abs/2008.08115) | False-positive/negative categories instead of an anecdotal image gallery |
| 15 | COCO's [official evaluator contract](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py) | Score ordering, precision/recall, interpolation, AP, and threshold tradeoffs |
| 16 | ONNX [IR](https://onnx.ai/onnx/repo-docs/IR.html), [versioning](https://onnx.ai/onnx/repo-docs/Versioning.html), and PyTorch's [ONNX exporter](https://docs.pytorch.org/docs/stable/onnx.html) | Export manifest plus pre-NMS numerical parity on identical tensors |
| 17 | [SORT](https://arxiv.org/abs/1602.00763), MIT [Kalman-filter notes](https://ocw.mit.edu/courses/2-160-identification-estimation-and-learning-spring-2006/resources/lecture_5/), and SciPy [`linear_sum_assignment`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html) | Motion state, gated global assignment, and explicit track lifecycle |
| 18 | TensorRT [benchmarking guidance](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html) and [Nsight Systems](https://docs.nvidia.com/nsight-systems/UserGuide/) | Warmed stage-level latency distributions and an end-to-end timeline |
| 19 | [Model Cards](https://arxiv.org/abs/1810.03993), TIDE, and Stanford [CS329S materials](https://stanford-cs329s.github.io/syllabus.html) | Named failure slices, operational limits, and monitoring hypotheses |
| 20 | TensorRT [accuracy considerations](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/accuracy-considerations.html) and [engine compatibility](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/engine-compatibility.html) | Per-target FP32/FP16 build, parity, memory, and latency evidence |
| 21 | NVIDIA [JetPack archive](https://developer.nvidia.com/embedded/jetpack-archive) and archived Nano [power-management guide](https://docs.nvidia.com/jetson/archives/l4t-archived/l4t-3275/Tegra%20Linux%20Driver%20Package%20Development%20Guide/power_management_nano.html) | Immutable target inventory and controlled power/thermal conditions |
| 22 | [Model Cards](https://arxiv.org/abs/1810.03993) and ACM-style [artifact evaluation criteria](https://sigsim.acm.org/conf/pads/2024/blog/artifact-evaluation/) | Claims, limitations, commands, and artifacts another engineer can audit |

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
