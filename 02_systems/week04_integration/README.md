# Week 4 lab: Bounded parallel frame pipeline

This review lab applies process/resource vocabulary, memory-layout awareness,
and the week 3 queue to a small perception-shaped workload. It deliberately does
not involve a camera or ML framework yet.

## Prepare

**Required concepts**

- Revisit OSTEP [Chapter 30: Condition
  Variables](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-cv.pdf) and C++ Core
  Guidelines [CP.20, CP.23, and
  CP.42](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rconc-wait).
  Before coding, draw producer, bounded queue, workers, ordered result slots,
  close, and join. Add a separate exception path and assign ownership at every
  transition.
- Before benchmarking, read the official [Google Benchmark methodology and
  reporting guide](https://google.github.io/benchmark/user_guide.html). Use its
  treatment of warmup, repetitions, medians, and dispersion to plan the worker
  count/capacity matrix; one fast run is not evidence of a speedup.

**API references while coding**

- Use Microsoft's [`std::thread`
  reference](https://learn.microsoft.com/en-us/cpp/standard-library/thread-class?view=msvc-170)
  to verify ownership, `joinable`, and `join` contracts. For the failure
  rehearsal, specify the policy first, then consult the standard [`<exception>`
  facilities](https://learn.microsoft.com/en-us/cpp/standard-library/exception?view=msvc-170)
  for transporting a captured failure to its owner.

**Optional / after the first attempt**

- Compare your policy note with GStreamer's production [`appsink` queue
  controls](https://gstreamer.freedesktop.org/documentation/app/appsink.html)
  and [latency design](https://gstreamer.freedesktop.org/documentation/additional/design/latency.html).
  Identify which setting corresponds to blocking, dropping oldest, and dropping
  newest; do not retrofit those policies into the generic queue.
- After collecting scaling data, read Intel oneTBB's [bandwidth and cache
  affinity](https://www.intel.com/content/www/us/en/docs/onetbb/developer-guide-api-reference/2021-11/bandwidth-and-cache-affinity.html)
  discussion and test whether memory bandwidth or cache locality plausibly
  explains where more workers stopped helping.

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
