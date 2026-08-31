# Chapter 08 — Interviews and Evidence

**Weeks:** 18–26  
**Outcome:** you can solve familiar patterns under time pressure, design an edge
inference system aloud, and support every resume claim with an artifact.

This chapter runs in parallel with the capstone. Application timing follows the
role-specific evidence you can already defend, not a curriculum date. The course
expands the radius of defensible applications; it is not a six-month employment
embargo.

## Three application tracks

- **Track A — apply immediately:** your existing production-SWE experience may
  already support general/early-career SWE, backend, mission or manufacturing
  software, and bridge roles inside robotics, defense, or industrial companies.
  This curriculum is not a prerequisite for those applications.
- **Track B — expand as evidence appears:** add C++ systems,
  embedded-adjacent, hardware/software integration, robotics-adjacent, factory
  automation, and device-interface roles when the corresponding C++/systems
  artifacts exist and you can explain them truthfully.
- **Track C — evidence-gated specialist roles:** make CUDA/GPU, perception/CV,
  edge inference, and TensorRT-heavy roles serious targets once the relevant
  kernels, evaluation, deployment, and measurements actually exist.

Applying early does not authorize unsupported claims. A role can sit in a
different track for you than for someone else; the evidence you can defend is the
boundary.

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

Outside that weekly loop, use the
[interview reconnaissance protocol](interview_recon.md) once when a serious role
search begins, before a specific interview loop, and optionally every 4–6 weeks
while targets are changing. It is not recurring weekly homework. Start each
session from [the reusable template](interview_recon.template.md).

## Target-specific emphasis

For perception/CV/ML roles, lead with C++, CUDA, model evaluation, inference
deployment, and the detect-track measurements. Be ready to trace one frame through
memory layouts, preprocessing, the model, postprocessing, association, and output.

For a field/deployment engineering parallel track, also complete
[operational_decomposition.md](operational_decomposition.md). The exercise is about
objects, actions, permissions, failure recovery, and evaluation—not vendor jargon.

## Track C specialist-evidence gate

- [ ] Capstone accuracy and latency commands reproduce
- [ ] You can implement BFS and a bounded concurrent queue without notes
- [ ] You can explain precision, recall, PR curves, AP, and threshold tradeoffs
- [ ] You can point to one kernel and explain its measured bottleneck
- [ ] You can explain why FP16 changed (or did not change) latency
- [ ] Every numerical resume claim has an evidence location
- [ ] You have rehearsed a five-minute and a fifteen-minute capstone walkthrough

These checks expand specialist targeting; they do not block Track A or every
Track B application. If a gate is false, target only roles for which you can
describe the gap truthfully. Do not fabricate certainty or performance.
