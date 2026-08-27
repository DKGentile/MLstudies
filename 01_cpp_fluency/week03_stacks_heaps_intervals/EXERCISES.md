# Week 3 exercises

## A. Contract implementation

Implement every `TODO` in `starter/week03.cpp`. Above the monotonic-stack loop,
write what remains unresolved on the stack. Above the interval loop, write what
the output's final interval represents.

Add adversarial tests for deep nesting, equal temperatures, duplicate heap
values, fully contained intervals, and negative endpoints.

## B. Streaming top-k experiment

Generate a deterministic stream of at least one million integers. Maintain the
largest 100 values without storing a second full copy. Record peak container
size and elapsed time. Compare with sorting a copy and explain when the heap
approach wins even if the benchmark timing is noisy.

## C. Problem pack

Use LeetCode 20, 155, 739, 215, 347, 56, 57, and 435. Complete five, including
at least one from each pattern family. For interval problems, write "sorted by
____ because ____" before coding.

## D. Recall gate

The next morning, implement a min-oriented `std::priority_queue` declaration,
a bracket matcher, and interval merge from memory in 20 minutes.

