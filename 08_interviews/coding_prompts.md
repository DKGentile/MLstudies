# Timed Coding Prompts

## Prepare

Use Princeton's [Algorithms lecture map](https://algs4.cs.princeton.edu/lectures/)
to review only a weak pattern: stacks/queues, analysis, union-find, priority
queues, symbol tables, or graphs. For BFS/DFS/cycle/topological reasoning, MIT's
[DFS lecture](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-10-depth-first-search/)
is the conceptual reference.

Do not watch a solution immediately before its matching prompt. Review the data
structure, wait at least a day, then solve from the contract. The score is based
on a stated invariant, tested implementation, complexity, and extension—not on
recognizing a memorized body.

Implement these in C++17 without looking up a full solution. Write your own tests
before checking an online equivalent. For each prompt, state the invariant,
complexity, and one production-oriented extension.

## Arrays, hashing, and windows

1. **Frame deduplicator (25 min):** Given frame hashes and a window size `k`, return
   the first pair of equal hashes at most `k` positions apart. Target O(n) time.
2. **Longest stable exposure (30 min):** Given integer brightness samples, find the
   longest contiguous range where `max - min <= tolerance`. Target O(n) with two
   monotonic deques.
3. **Detection-rate budget (25 min):** Find the minimum-length contiguous interval
   whose summed processing time reaches a required budget. State when the usual
   sliding window fails.
4. **Sparse class counts (25 min):** Return the `k` most frequent class IDs with a
   deterministic tie rule. Discuss heap versus bucket approaches.

## Search, heaps, and intervals

5. **Batch-size chooser (30 min):** Given a monotonic predicate
   `fits_in_memory(batch)`, return the largest feasible positive batch. Specify
   behavior when none fit and avoid overflow.
6. **Camera reservation merge (25 min):** Merge overlapping half-open recording
   intervals. Explain why endpoint semantics matter.
7. **GPU job scheduler (35 min):** Given arrival time and duration, output completion
   order for a non-preemptive shortest-job-first worker. Use a heap.
8. **Top-k latency stream (30 min):** Maintain the `k` largest latencies seen so far
   and return them sorted at the end. Explain memory bounds.

## Trees and graphs

9. **Pipeline build order (30 min):** Given named stages and dependencies, return a
   deterministic topological order or a cycle error.
10. **Sensor connectivity (30 min):** Process cable additions and connectivity
    queries online. Implement union-find with path compression and union by size.
11. **Nearest healthy node (25 min):** In an unweighted network, find the closest
    healthy compute node and reconstruct the path. Use BFS.
12. **Failure-domain count (25 min):** Count connected components in a grid with
    4-neighbor connectivity; then discuss recursion depth.
13. **Configuration inheritance (35 min):** Detect a cycle in a directed graph and
    return one concrete cycle, not only a boolean.

## Systems-flavored

14. **Bounded blocking queue (45 min):** Reimplement the chapter queue from memory.
    Define close/shutdown semantics and write a two-producer/two-consumer test.
15. **LRU tensor cache (35 min):** Implement `get`/`put` in O(1). State ownership and
    thread-safety assumptions.
16. **Ring buffer (35 min):** Fixed-capacity frame ring with overwrite-oldest
    semantics. Distinguish empty from full without sacrificing clarity.
17. **Rate limiter (35 min):** Implement a token bucket using an injected monotonic
    clock so tests do not sleep.
18. **Shape-safe arena (45 min):** Design an API that reuses byte buffers for tensor
    shapes without returning undersized memory. Focus on invariants and overflow.

## Review protocol

After time expires, mark one of:

- `independent`: correct, tested, and explained inside the limit;
- `debugged`: right approach, needed extra time to fix;
- `hinted`: needed a conceptual hint;
- `review`: could not establish a viable invariant.

Retry `debugged` after three days and `hinted/review` the next morning. Count a
problem only when it becomes `independent`.
