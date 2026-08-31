# Week 3 exercises

## Core

1. Implement the five `TODO` methods in `bounded_queue.hpp`.
2. Add a test with at least four producers and two consumers. Each producer owns
   a disjoint numeric range; prove every value is consumed exactly once.
3. Add temporary counters for blocked pushes, blocked pops, and maximum queue
   depth. Log results for multiple capacities, then decide whether to keep the
   counters behind an optional diagnostics interface.
4. Explain the happens-before relationship that makes an inserted item visible
   to a consumer after lock transfer.

## Failure injection

Perform one change at a time, predict, test, and revert:

- replace a predicate wait with a bare wait;
- notify before changing the guarded state;
- use two different mutexes for the deque and closed flag;
- notify one waiter during close instead of all;
- access `closed_` without its mutex.

## Intentional bug clinic

Configure the opt-in `systems_race_clinic` target described in the README. Before
editing it:

1. reproduce the workload in a normal debugger build and inspect the worker
   threads, call stacks, and shared metrics object;
2. run it under ThreadSanitizer on Linux/WSL and save the first report;
3. name the two conflicting accesses and explain why the start flag and later
   `join()` do not synchronize worker-to-worker counter updates;
4. implement one justified repair, rerun ThreadSanitizer, and confirm both a clean
   diagnostic and exact totals.

Do not add the clinic to CTest or make it part of the default build. Its initial
race is curriculum input, not an accidental repository failure.

## Stretch

Design (do not immediately implement) `try_push`, `try_pop`, and timed waits.
Specify how timeout competes with closure and an item becoming available. Only
implement after writing deterministic-enough contract tests.
