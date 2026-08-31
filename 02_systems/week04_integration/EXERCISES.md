# Week 4 exercises

## Core

1. Implement `process_frames` with the week 3 bounded queue. Preserve input
   positions independently of sequence values and join every thread on every
   path.
2. Implement the fixed-width, big-endian frame encoder and incremental decoder.
   Make all supplied protocol tests pass, then add one count/length mismatch and
   one awkward chunk sequence of your own.
3. Implement `write_all`. Use the scripted short-writer tests; do not assume a
   blocking socket makes partial success impossible.
4. Implement `receive_and_process_frames` as a live receive-to-bounded-queue
   pipeline. Do not accumulate the entire connection before worker processing.
5. Pass the scripted-read, real-loopback, clean half-close, and truncated-close
   contracts. Add one empty-stream test and one duplicate-sequence test.
6. Draw ownership and shutdown for normal empty input, normal nonempty input,
   mid-frame EOF, socket error, and worker exception.

## Required observation and measurement

1. Before the first run, write the required TCP/UDP comparison from the README;
   keep the primary implementation on TCP.
2. Run the two supplied probe processes with send/receive chunk limits above and
   below the four-byte prefix. Predict whether each call produces zero, one, or
   multiple frames before running it.
3. Inspect one connection with `ss` on Linux/WSL (or
   `Get-NetTCPConnection` on Windows), then use `tcpdump` if available. Explain
   why the observed segments cannot define the application framing contract.
4. Inject temporary worker delay and compare queue capacities 1, 4, and 16.
   Capture queue depth, sender elapsed time, and socket queues; give a causal
   backpressure explanation and then remove the delay.
5. Rehearse disconnects at three byte offsets: partial prefix, partial body, and
   exact boundary. Verify cleanup completes within the CTest timeout.
6. Run representative `(worker_count, capacity)` pairs rather than the former
   exhaustive matrix. Record warmup, five repetitions, median throughput, input
   bytes, and the first point where more workers stop helping.

## Debugging integration

Complete the opt-in Week 3 race clinic before adding shared pipeline metrics.
For any metric updated by several workers, state its synchronization owner or
reduction rule. A ThreadSanitizer-clean run is evidence about the exercised
workload, not a proof that all interleavings are safe.

## Optional variation (choose at most one)

- implement a small UDP datagram probe that tests one claim from the required
  TCP/UDP comparison;
- implement a deliberate drop-oldest policy in a separate queue type;
- change the worker calculation to a histogram with per-worker bins and merge;
- run the receiver through Week 1's process runner and compare failure isolation;
- add an explicit end-of-stream control frame and compare it with boundary EOF.

Each implemented variation needs a prediction, contract test, and measured
evidence. Do not start an HTTP/RPC framework or nonblocking event loop.

## Interview rehearsal

In five minutes, answer: "Design a TCP-connected capture-to-inference pipeline
when a sensor produces 60 FPS but inference sustains 40 FPS." State framing,
maximum message size, latency goal, queue/backpressure or drop policy, shutdown
and truncated-frame behavior, timeout boundaries, metrics, and one failure mode.
