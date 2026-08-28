# Design Prompt — On-Device Detection Pipeline

You have 45 minutes. Design a four-camera, on-device object-detection and tracking
system. The device has constrained GPU memory, intermittent connectivity, and a
requirement to emit an alert within 150 ms at p95. Operators need short evidence
clips, but raw video should not normally leave the device.

## Prepare

Before attempting the prompt, review Stanford's [CS329S ML systems materials](https://stanford-cs329s.github.io/syllabus.html)
for the lifecycle from requirements and data through deployment and monitoring,
and Google SRE's [Reliable Product Launches](https://sre.google/sre-book/reliable-product-launches/)
for canary, rollback, capacity, and operational readiness. Extract questions and
mechanisms; the design must still be derived from this prompt's constraints.

## Clarify first

Ask about object classes, camera resolution/FPS, alert volume, acceptable misses,
power/thermal limits, retention, privacy, offline duration, update safety, and the
meaning of the 150 ms boundary.

## Cover

- capture, buffering, backpressure, and dropped-frame policy;
- batching versus per-stream latency;
- preprocess, inference, postprocess, and tracker state;
- model/runtime versioning and rollback;
- metrics for accuracy, latency, queue depth, thermals, and data drift;
- behavior during camera, GPU, storage, or network failure;
- evidence-clip encryption, retention, and upload retries;
- canary deployment and a representative offline eval set.

## Follow-ups

1. GPU utilization is only 40%, but p95 is 280 ms. What do you measure next?
2. Night recall drops after a camera firmware update. How do you isolate the cause?
3. The new model is faster but causes twice as many fragmented tracks. Roll out?
4. One camera produces frames faster than the others. How do you protect fairness?

Score with [../mock_scorecard.md](../mock_scorecard.md), emphasizing explicit
tradeoffs and observability over naming products.
