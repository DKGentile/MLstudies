# Results

## Prepare

Read the original [Model Cards paper](https://arxiv.org/abs/1810.03993) for the
categories a responsible model report should expose, and the original
[TIDE paper](https://arxiv.org/abs/2008.08115) for detection-error categories.
Use ACM-style [artifact evaluation criteria](https://sigsim.acm.org/conf/pads/2024/blog/artifact-evaluation/)
as a final test of whether another engineer can obtain the artifacts and exercise
the documented workflow.

Before writing conclusions, separate measured results, derived quantities,
hypotheses, and unmeasured claims. Each number must identify data split, model
hash, runtime, hardware, input shape, precision, and command or source artifact.

Commit compact evidence here: CSV summaries, learning curves, carefully selected
annotated stills, and written failure analysis. Large videos, model weights, engine
files, and profiler captures are ignored by Git.

Copy the templates before recording results:

- `benchmark.template.csv` — latency, throughput, memory, and methodology
- `accuracy.template.csv` — validation/test metrics tied to model hashes
- `failure_cases.template.md` — examples organized by cause, not anecdotes

The final report must distinguish measured values from estimates and mark missing
hardware results as `not measured`, never zero.
