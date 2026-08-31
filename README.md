# Embedded AI / ML Engineering Lab

A 26-week, code-first course for moving from production software engineering into
computer vision, GPU programming, and edge inference. The curriculum is organized
as a sequence of labs, not a reading list: each chapter has starter code, explicit
constraints, tests, and an artifact to measure.

The destination is one defensible portfolio project: **`edge-detect-track`**. You
will train a small detector, implement the important parts of a tracker, export it,
benchmark it, and document deployment tradeoffs on desktop and Jetson hardware.

## Start here

1. Read [SETUP.md](SETUP.md) and run the environment doctor:

   ```powershell
   python scripts/doctor.py
   ```

2. Read [LEARNING_GUIDE.md](LEARNING_GUIDE.md). It explains the red-test workflow
   and what counts as completing a lab.
3. Pick a Monday and generate your calendar:

   ```powershell
   python scripts/make_schedule.py --start 2026-08-31
   ```

4. Open [01_cpp_fluency](01_cpp_fluency) and begin Week 1.
5. Copy [progress/weekly_log.template.md](progress/weekly_log.template.md) to a
   private working log, or edit it in place if you want your learning history in
   Git.

You do **not** need a GPU for the first five weeks. GPU labs detect missing tooling
and explain what can still be completed on CPU.

## Course map

| Chapter | Weeks | What you build | Exit artifact |
|---|---:|---|---|
| [01 · C++ Fluency](01_cpp_fluency) | 1–4 | Algorithms plus ownership, RAII, moves, and debugging | Tested patterns + move-only buffer evidence |
| [02 · Systems](02_systems) | 1–4 | Processes, memory, concurrency, TCP framing, and backpressure | Bounded network-to-worker pipeline |
| [03 · ML Fundamentals](03_ml_fundamentals) | 3–6 | NumPy models, losses, gradients, regularization | Logistic regression and two-layer net from scratch |
| [04 · Computer Vision](04_computer_vision) | 5–9 | Image operators, a small CNN, and camera geometry | CNN report + tested projection primitives |
| [05 · CUDA](05_cuda) | 6–12 | Kernels from indexing through reduction and blur | Correct CUDA kernels with CPU references |
| [06 · GPU Optimization](06_gpu_optimization) | 11–14 | Reproducible profiling and optimization | Two-GPU benchmark report |
| [07 · Edge Detect + Track](07_edge_detect_track) | 10–22 | Detector, evaluation, tracker, ONNX, TensorRT, Jetson | Measured end-to-end capstone |
| [08 · Interviews + Evidence](08_interviews) | 18–26 | Timed drills, design exercises, evidence, market calibration | Evidence packet + dated reconnaissance |

The phases overlap deliberately. See [COURSE_MAP.md](COURSE_MAP.md) for the
week-by-week route and gates.

## Applications while learning

This curriculum expands the radius of roles you can defend; it is not a
six-month embargo on applying. Apply immediately to general or bridge SWE roles
already supported by your professional evidence. Expand into C++/systems and
hardware-integration roles as those artifacts appear. Treat CUDA, perception,
edge-inference, and TensorRT-heavy roles as evidence-gated specialist targets.
See the [three-track model](08_interviews/README.md#three-application-tracks) and
keep every claim truthful.

## The daily loop

1. Complete the local `Prepare` assignment and answer its ready-to-code check
   without the source open.
2. Implement the starter exercise without an assistant-generated solution.
3. Run the nearest test; use the failure as feedback.
4. When a clinic calls for it, reproduce the fault under a debugger or sanitizer,
   name the root cause, repair it, and rerun the same diagnostic.
5. Explain the invariant, ownership rule, complexity, or performance model aloud.
6. Use the after-first-attempt resource only for a concrete gap or result.
7. Record a number, failure, diagnostic, or decision in your weekly log.

Use AI as a reviewer after Weeks 1–2: ask it to identify counterexamples, critique
a benchmark, or question an explanation. The point of this repository is to make
the keystrokes and debugging yours.

## Useful commands

```powershell
# Show environment capabilities without installing anything
python scripts/doctor.py

# Print the work assigned to one week
python scripts/course.py week 7

# Check that the course scaffold is internally consistent
python scripts/validate_repo.py

# Run safe scaffold checks; Python learner challenges skip until explicitly enabled
python -m pytest -q
```

Each chapter documents its own build and test commands. No script automatically
downloads datasets, model weights, or paid course material.

## Ground rules

- Commit after a coherent exercise, not after every typo.
- Reproduce a bug before repairing it; do not silence a diagnostic you cannot
  explain.
- Never claim a GPU number without warmup, synchronization, and repeated samples.
- TensorRT engines are target-specific artifacts. Export ONNX once; build an engine
  on each deployment target.
- Store measurements and small plots in Git. Do not commit datasets, weights,
  TensorRT engines, videos, or profiler captures.
- A completed, measured desktop deployment is better than an unfinished Jetson
  port. Time-box legacy Nano work to one weekend.

The source curriculum is mapped in [docs/curriculum_mapping.md](docs/curriculum_mapping.md),
and the volatile toolchain assumptions are isolated in
[docs/compatibility.md](docs/compatibility.md).
