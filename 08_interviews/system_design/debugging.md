# Design Prompt — Debug a Latency Regression

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

