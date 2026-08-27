# Week 4 lab: Bounded parallel frame pipeline

This review lab applies process/resource vocabulary, memory-layout awareness,
and the week 3 queue to a small perception-shaped workload. It deliberately does
not involve a camera or ML framework yet.

## Build target

Implement `process_frames` in `starter/frame_pipeline.cpp`. The pipeline accepts
frames containing signed samples and computes peak-to-peak amplitude with a
fixed worker count and bounded queue capacity.

Required design:

1. one producer submits frames to `BoundedQueue`;
2. the requested number of worker threads consume and compute;
3. completion closes/unblocks the correct stages;
4. results return in input order even when workers finish out of order;
5. all threads are joined on success and exceptions;
6. shared result state has an explicit synchronization owner.

Do not replace this with `std::async` per frame or an unbounded vector of
threads. The bounded resource is the point of the lab. Empty sample arrays have
amplitude zero. Use wide intermediate arithmetic before narrowing to the public
`long long` result type.

## Experiments

Generate deterministic frames large enough for measurable work, then run worker
counts 1, 2, 4, and 8 with capacities 1, 4, 16, and 64. Log:

- frame/sample counts and total input bytes;
- wall time and frames/second;
- maximum queue depth (temporary instrumentation);
- whether output order stayed stable;
- the point where more threads stopped helping and your explanation.

Watch CPU utilization and process memory. Explain why worker count, queue depth,
and resident working set are connected. Do not claim a speedup from one run;
warm up and report at least a median of five.

## Failure rehearsal

Inject one worker exception for a chosen sequence number. Before coding a
recovery, specify ownership, how blocked threads wake, how the first exception
reaches the caller, and whether partial results are returned. Add a test, then
implement and document the policy.

## Phase 0 systems exit

Reimplement a small `BoundedQueue<int>` from memory. Then explain this pipeline
using a state diagram with producer, queue, workers, result slots, close, and
join. If either task requires copying the starter, repeat week 3's recall drill.

