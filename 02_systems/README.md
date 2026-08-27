# Systems Refresh: Phase 0

This four-week module turns the selected OSTEP chapters into small programs you
can inspect, break, and repair. It is intentionally narrow: processes, address
spaces, threads, and locks, followed by one bounded worker-pipeline integration.
Those concepts recur in data loaders, camera pipelines, inference workers, and
GPU runtimes.

## Study loop

For each lab:

1. Read only the assigned OSTEP chapters from the
   [official free book site](https://pages.cs.wisc.edu/~remzi/OSTEP/).
2. Draw the mechanism before coding: process/resources, virtual-to-physical
   mapping, or the queue state and wait conditions.
3. Implement the `TODO`s without changing the public contract.
4. Run the contract test, then the observation commands in the lab README.
5. Put measured evidence in `progress/experiment_log.csv` and explain one
   surprise in `progress/LAB_REPORT.md`.

Starter functions deliberately throw `TODO` errors. Tests are executable
specifications and initially fail. Platform-specific implementations belong
behind `#if defined(_WIN32)` / POSIX branches, not in duplicated public APIs.

## Map

| Week | Reading and lab | Deliverable |
|---|---|---|
| 1 | OSTEP processes, chapters 4-5; spawn, capture, and wait | portable child-process runner plus process tree notes |
| 2 | address spaces/VM, chapters 13-15; allocate and touch pages | address/page probe with before/after memory observations |
| 3 | threads and locks, chapters 26-29; condition variables | bounded blocking queue that passes concurrency contracts |
| 4 | review and integration | bounded multi-worker frame pipeline plus failure analysis |

## Build and test

You need CMake 3.21+ and a C++17 compiler:

```text
cmake --preset default
cmake --build --preset default
ctest --preset default
```

PowerShell and POSIX wrappers live in `scripts/`. Invoke them with
`powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_checks.ps1`
or `sh scripts/run_checks.sh` if direct script execution is disabled. A focused
run looks like:

```text
ctest --test-dir build -C Debug -R systems_week03 --output-on-failure
```

The Windows process implementation should use native process/pipe APIs; the
POSIX implementation should use process/pipe/wait APIs. Do not make the tests
pass by invoking a shell with a concatenated untrusted command string.

## Definition of done

You can, from memory:

- distinguish a process from a program and identify what `exec` replaces;
- explain why reserving virtual memory and touching resident pages differ;
- write a blocking queue whose wait is guarded by a predicate;
- explain close/drain semantics and why notifications occur after state change;
- support claims with PID, byte count, elapsed time, or observed state.
