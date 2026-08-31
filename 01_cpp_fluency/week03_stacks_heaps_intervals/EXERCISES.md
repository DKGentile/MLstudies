# Week 3 exercises

## A. Contract implementation

Implement every `TODO` in `starter/week03.cpp`. Above the monotonic-stack loop,
write what remains unresolved on the stack. Above the interval loop, write what
the output's final interval represents.

Add adversarial tests for deep nesting, equal temperatures, duplicate heap
values, fully contained intervals, and negative endpoints.

## B. Move-only ownership contract

Complete the Week 3 section of
[`modern_cpp_engineering/EXERCISES.md`](../modern_cpp_engineering/EXERCISES.md).
Implement the `OwnedBuffer` resource operations, add the required move-chain and
scope/container tests, and draw ownership before and after each move. The public
compile-time copy/move checks are part of the contract, not tests to weaken.

## C. Problem pack

Use LeetCode 20, 155, 739, 215, 347, 56, 57, and 435. Complete four, including
at least one from each pattern family. The ownership implementation replaces
one item of duplicate practice volume. For interval problems, write "sorted by
____ because ____" before coding.

## D. Recall gate

The next morning, implement a min-oriented `std::priority_queue` declaration,
a bracket matcher, and interval merge from memory in 20 minutes.

## E. Optional after first attempt: streaming top-k experiment

Generate a deterministic stream of at least one million integers. Maintain the
largest 100 values without storing a second full copy. Record peak container
size and elapsed time. Compare with sorting a copy and explain when the heap
approach wins even if the benchmark timing is noisy. Do this after the algorithm
contracts and move-only owner are implemented.
