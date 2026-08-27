# How to Use This Repository

This repository contains **starter implementations**, not answer keys. Search for
`LEARNER TODO` to find work. Exercise tests are executable specifications and are
expected to fail until the corresponding TODO is complete.

## A lab session

1. Read the chapter's `README.md` and the exercise docstring.
2. Predict the output, complexity, and likely failure cases before coding.
3. Run the smallest relevant test once to see its contract.
4. Implement only enough to make one new case pass.
5. Add at least one adversarial test that was not supplied.
6. Run with warnings/sanitizers or a profiler when the chapter asks for it.
7. Write the result in the log using evidence: input size, median time, hardware,
   and software versions.

## Red tests versus repository validation

There are two kinds of checks:

- `python scripts/validate_repo.py` validates links in the course manifest, parses
  Python files, and checks required learning markers. It should pass on a fresh
  clone.
- Chapter exercise tests describe the behavior you must implement. Python chapters
  require the environment opt-in documented in their README; once enabled, they
  may fail with `NotImplementedError` until solved. Native C++/CUDA exercise
  binaries begin red as soon as they are built. That is the starting line.

Never make a test green by weakening or deleting its assertion. If you think a test
is wrong, write the counterexample in your log first.

## What AI help is useful

During Weeks 1–2, keep implementation work unaided. Later, useful review prompts
include:

- “Give me three counterexamples for this interface; do not write the solution.”
- “Audit this benchmark methodology for synchronization and warmup errors.”
- “Interview me about this kernel and challenge vague claims.”
- “Review my derivation and point to the first invalid step.”

Avoid pasting a TODO and asking for finished code. You would be optimizing the wrong
metric: repository completion instead of recall and judgment.

## Definition of a useful number

A benchmark record includes:

- exact device and software versions;
- input shape, batch size, precision, and preprocessing;
- warmup count, measured iterations, and synchronization method;
- median and tail latency (at least p95), not only the best run;
- correctness tolerance or accuracy metric;
- the exact command and Git commit.

FPS is derived from end-to-end latency only when the pipeline truly processes one
frame at a time. Report model-only and end-to-end timing separately.

## When to move on

Finish the required tests, the recall drill, and the artifact named in the chapter.
Optional stretch exercises are explicitly labeled. If a hardware issue consumes a
full planned session, record it and use the CPU/reference path until the scheduled
hardware-debug block.
