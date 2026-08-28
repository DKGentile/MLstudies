# Chapter 08 — Interviews and Evidence

**Weeks:** 18–26  
**Outcome:** you can solve familiar patterns under time pressure, design an edge
inference system aloud, and support every resume claim with an artifact.

This chapter runs in parallel with the capstone. Start applications when the
capstone contains reproducible accuracy and latency numbers—not when the calendar
reaches a particular date.

## Weekly preparation route

The preparation is deliberately short. Read the named source, then rehearse with
your own code and artifacts; reading does not count as interview practice.

| Week | Core source | Rehearsal focus |
|---:|---|---|
| 18 | Princeton [Algorithms lectures](https://algs4.cs.princeton.edu/lectures/) and MIT [DFS/topological sort](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-10-depth-first-search/) | State an invariant and complexity before timed graph/heap/union-find code |
| 19 | Stanford [CS329S ML systems materials](https://stanford-cs329s.github.io/syllabus.html) | Requirements, data, deployment, monitoring, and feedback loops for edge inference |
| 20 | TensorRT [benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html) and [accuracy considerations](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/accuracy-considerations.html) | Defend timing boundaries, synchronization, and FP16 evidence |
| 21 | Google SRE: [Reliable Product Launches](https://sre.google/sre-book/reliable-product-launches/) | Canary, rollback, kill switches, and legacy-target deployment risk |
| 22 | Original [Model Cards paper](https://arxiv.org/abs/1810.03993) | Audit every resume/model claim against an artifact and named limitation |
| 23 | Google SRE: [Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/), [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/), and [Postmortem Culture](https://sre.google/sre-book/postmortem-culture/) | Diagnose a regression using boundaries, distributions, causal tests, rollback, and prevention |
| 24 | CUDA [Best Practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/) and Nsight Compute [Profiling Guide](https://docs.nvidia.com/nsight-compute/ProfilingGuide/) | Re-derive one optimization and defend the profiler evidence |
| 25 | ACM-style [artifact evaluation criteria](https://sigsim.acm.org/conf/pads/2024/blog/artifact-evaluation/) | Ten-minute walkthrough centered on artifacts another engineer can exercise |
| 26 | NeurIPS [paper checklist guidelines](https://neurips.cc/public/guides/PaperChecklist) | Final audit of claims, assumptions, splits, run counts, environment, uncertainty, and limitations |

## Weekly loop

- Five 25–35 minute coding sessions from [coding_prompts.md](coding_prompts.md) or
  your existing pattern list.
- One 45-minute design prompt from [system_design](system_design).
- One 30-minute project walkthrough recorded locally.
- Friday: update [evidence_matrix.template.md](evidence_matrix.template.md) and
  choose one weak claim to strengthen or remove.
- Every other week: a full mock using [mock_scorecard.md](mock_scorecard.md).

## Target-specific emphasis

For perception/CV/ML roles, lead with C++, CUDA, model evaluation, inference
deployment, and the detect-track measurements. Be ready to trace one frame through
memory layouts, preprocessing, the model, postprocessing, association, and output.

For a field/deployment engineering parallel track, also complete
[operational_decomposition.md](operational_decomposition.md). The exercise is about
objects, actions, permissions, failure recovery, and evaluation—not vendor jargon.

## Application gate

- [ ] Capstone accuracy and latency commands reproduce
- [ ] You can implement BFS and a bounded concurrent queue without notes
- [ ] You can explain precision, recall, PR curves, AP, and threshold tradeoffs
- [ ] You can point to one kernel and explain its measured bottleneck
- [ ] You can explain why FP16 changed (or did not change) latency
- [ ] Every numerical resume claim has an evidence location
- [ ] You have rehearsed a five-minute and a fifteen-minute capstone walkthrough

If a gate is false, keep applying selectively only when you can describe the gap
truthfully. Do not fabricate certainty or performance.
