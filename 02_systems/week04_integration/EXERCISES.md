# Week 4 exercises

## Core

1. Implement `process_frames` with the week 3 bounded queue.
2. Add a deterministic test with at least 1,000 frames and repeated sequence
   numbers; ordering is by input position, not by sequence uniqueness.
3. Add temporary timing around submission, worker computation, and final join.
   Identify which stage limits throughput for two workloads.
4. Draw the shutdown protocol for normal empty input, normal non-empty input,
   and a hypothetical worker exception.

## Applied variations

Choose two:

- change the calculation to a histogram with per-worker local bins and a merge;
- make frame payloads large and compare copying with safe move-based submission;
- implement a deliberate drop-oldest policy in a separate queue type;
- pin the process/threads using platform APIs and measure carefully;
- run the pipeline as a child using week 1's runner and compare failure isolation.

Each variation needs a prediction, a contract test, and measured evidence.

## Interview rehearsal

In five minutes, answer: "Design the capture-to-inference queue for an embedded
detector when the camera produces 60 FPS but inference sustains 40 FPS." State
latency goals, backpressure/drop policy, memory bound, shutdown semantics,
metrics, and one failure mode.

