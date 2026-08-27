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

## Stretch

Design (do not immediately implement) `try_push`, `try_pop`, and timed waits.
Specify how timeout competes with closure and an item becoming available. Only
implement after writing deterministic-enough contract tests.

