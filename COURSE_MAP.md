# 26-Week Course Map

The `Primary build` is the non-negotiable work. `Parallel maintenance` keeps older
skills warm without letting them take over the week. If life interrupts the plan,
move the dates; do not compress two weeks into one.

| Week | Primary build | Parallel maintenance | Gate |
|---:|---|---|---|
| 1 | C++ arrays, vectors, hashing, two pointers | Processes lab; NumPy indexing | Explain contiguous storage and amortized growth |
| 2 | Binary search, sliding windows; storage lifetime and borrowing | Address-space lab; debugger/ASan clinics; NumPy broadcasting | State the monotonic predicate and diagnose invalid memory access |
| 3 | Stacks, heaps, intervals; RAII and move-only ownership | Thread/TSan clinic; linear/logistic regression | Move an owning buffer safely; benchmark a mutex queue; pass a gradient check |
| 4 | Trees, graphs, union-find, topo sort | TCP framing/network-to-worker pipeline; Rule of Zero/Five; regularization | Implement BFS/DSU and explain partial I/O, shutdown, and backpressure |
| 5 | kNN, softmax, validation discipline | Five C++ pattern problems | Produce a leakage-free experiment table |
| 6 | Two-layer network and backprop | CUDA indexing/vector-add lab | Numerical and analytic gradients agree |
| 7 | Convolution/pooling primitives | CUDA memory-access lab | Match a trusted CPU/NumPy reference |
| 8 | Small PyTorch CNN | Camera-frame notation prep; optional CUDA companion | Save train/validation curves and an overfit note |
| 9 | CUDA launch geometry; camera frames and pinhole projection | Capstone problem statement | Kernel handles awkward sizes; compose/invert a transform and project a world point |
| 10 | CUDA reduction | Capstone dataset audit | Dataset split and license documented |
| 11 | Histogram/atomics | Detector baseline setup | CPU/GPU correctness comparison recorded |
| 12 | Blur/convolution | First detector training run | Curves and environment manifest saved |
| 13 | Nsight profiling | Detector evaluation | Profile identifies a concrete bottleneck |
| 14 | One measured optimization | Baseline mAP/error analysis | Before/after table with sound timing |
| 15 | Detection metrics and thresholding | C++ maintenance | Explain precision/recall/AP from examples |
| 16 | ONNX export and parity | System-design sketch | Framework and ONNX outputs agree within tolerance |
| 17 | IoU association + track lifecycle | Timed graph problem | Tracker passes synthetic sequence tests |
| 18 | End-to-end tracked video | Five timed problems; first mock | Demo and latency breakdown exist |
| 19 | Failure-case collection | Design: edge inference pipeline | At least three named failure categories |
| 20 | TensorRT target build | Resume evidence draft | Reproducible FP32/FP16 benchmark |
| 21 | Jetson Nano time-boxed port | Mock interview | Nano result or written deferral decision |
| 22 | Freeze capstone README | Specialist applications expand as evidence gates pass | README contains mAP, latency, FPS, memory |
| 23 | Reliability and debugging review | Five timed problems | Explain one production failure end-to-end |
| 24 | Optimization review | Mock coding + design loop | Re-derive kernel speedup model |
| 25 | Portfolio walkthrough practice | Continue targeted applications; triggered reconnaissance as needed | Ten-minute artifact walkthrough is crisp |
| 26 | Final audit and retrospective | Close remaining weak pattern | All evidence is truthful and reproducible |

## Phase gates

Do not use calendar completion as proof of competence. Advance when these gates are
true:

- **C++ gate:** implement BFS, a bounded thread-safe queue, and the move-only
  buffer without reference code; explain ownership, borrowing, moved-from state,
  and deterministic destruction; compile new work warning-free.
- **Debugging gate:** given a debugger or sanitizer report, reproduce the fault,
  identify the first invalid lifetime/index/synchronization event, repair it,
  rerun the same diagnostic, and explain why the repair is correct.
- **Systems gate:** explain TCP stream semantics, length framing, partial I/O,
  byte order, EOF/truncated disconnects, graceful shutdown, and how a bounded
  queue propagates backpressure.
- **ML gate:** implement backprop for a tiny network and diagnose a widening
  train/validation gap.
- **CUDA gate:** explain coalescing, synchronization, and the measured bottleneck
  in one of your kernels.
- **Camera-geometry gate:** name coordinate frames, distinguish intrinsics from
  extrinsics, compose/invert rigid transforms, project through `K[R|t]`, and
  recover a normalized camera ray from a pixel.
- **Capstone gate:** another person can reproduce at least one accuracy number and
  one latency number from documented commands.

## Minimum viable week

When only five hours are available, do the chapter exercise, one test/debug loop,
and the weekly log. Skip optional video or reading before skipping code.
