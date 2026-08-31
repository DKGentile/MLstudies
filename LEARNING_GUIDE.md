# How to Use This Repository

This repository contains **starter implementations**, not answer keys. Search for
`LEARNER TODO` to find work. Exercise tests are executable specifications and are
expected to fail until the corresponding TODO is complete.

## A lab session

1. Complete the local `Prepare` or resource-route item for the exact week/lab.
   Close the source and answer its ready-to-code check in your own words.
2. Read the exercise contract, starter docstrings, and nearest tests.
3. Predict the output, complexity, invariant, and likely failure cases before coding.
4. Run the smallest relevant test once to see its contract.
5. Implement only enough to make one new case pass.
6. Add at least one adversarial test that was not supplied.
7. For a debugging clinic, reproduce the failure before editing, inspect it with
   the assigned debugger/sanitizer, and save the first causal diagnostic.
8. Repair the cause, rerun the same diagnostic configuration, and explain why
   the report disappeared rather than merely suppressing it.
9. Write the result in the log using evidence: input size, median time, hardware,
   and software versions.

## Debugger and sanitizer method

Warnings and dynamic diagnostics are learned competencies, not decorative flags.
Use a debugger to set a breakpoint, step into and over calls, inspect locals and
program state, read the call stack/backtrace, and inspect threads when concurrency
is involved. Start from a reproducible input and stop at the earliest state that
violates an ownership, bounds, or synchronization rule.

For an intentional clinic:

1. build the named opt-in target in its separate diagnostic build directory;
2. predict the bug class and run it unchanged;
3. capture the report, first invalid access, allocation/free or conflicting-access
   stacks, and exact command;
4. state the root cause in language terms—lifetime, bounds, data race, or another
   violated contract;
5. repair the cause without weakening the workload or disabling instrumentation;
6. rerun the same input and diagnostic; and
7. explain both why the repair establishes the required invariant and what the
   clean run does **not** prove.

AddressSanitizer and ThreadSanitizer are normally separate builds/runs. TSan is
not a native-MSVC route; use the documented Linux/WSL GCC/Clang configuration.
Intentional bug-clinic targets are opt-in and are never evidence that the normal
repository build is accidentally broken.

## How to use the resources

- **Core before coding** establishes the mechanism needed by the local exercise
  and checkpoint. Time-box it, take sparse notes, and then close it.
- **API reference while coding** answers contract and syntax questions. Consulting
  documentation is normal engineering; copying an exercise implementation is not.
- **Extension after first attempt** is for explaining an observed failure or
  comparing a completed baseline. Worked editorials belong here.

The local ready-to-code check is the gate between reading and implementation. If
you cannot answer it, return to the specific paragraph or lecture segment that
covers the gap instead of consuming another broad tutorial.

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

Before claiming a C++/systems gate, you must also be able to take an unfamiliar
debugger or sanitizer report through reproduce → root cause → repair → verified
rerun without silencing the diagnostic.
