# Design Prompt — Debug a Latency Regression

## Prepare

Read Google SRE's [Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/)
for the observe-hypothesize-test sequence and [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
for choosing actionable signals. For GPU/CPU timeline questions, know what
[Nsight Systems](https://docs.nvidia.com/nsight-systems/UserGuide/) records.

Do the prompt without reopening the sources. Every proposed measurement must
distinguish at least two hypotheses; every risky investigation needs a safe
rollback or load-reduction decision.

A release changes end-to-end p95 from 85 ms to 170 ms. Model-only median is
unchanged. Average GPU utilization is lower than before. No single error is obvious.

Drive the investigation. Your answer should include:

- a precise latency boundary and comparable before/after traffic;
- per-stage distributions rather than averages;
- queue depth, batching, synchronization, copies, allocation, decode, render, and
  I/O hypotheses;
- profiler/trace placement and correlation identifiers;
- a safe rollback or traffic-reduction decision;
- one experiment that distinguishes each leading hypothesis;
- how you prevent recurrence with a performance gate.

The interviewer should challenge any leap from correlation to root cause.
