# Week 1: Arrays, hashing, and two pointers

## Mental models

- A `std::vector` stores elements contiguously: indexing is constant time and
  sequential scans are cache-friendly. Inserting at the front is not free.
- A hash table trades ordering and some memory for average constant-time key
  lookup. Correctness cannot depend on iteration order.
- Two pointers are useful when progress at one boundary lets you discard work
  at the other. State the reason a pointer move is safe.

Read one short reference for
[`std::vector`](https://en.cppreference.com/w/cpp/container/vector) and
[`std::unordered_map`](https://en.cppreference.com/w/cpp/container/unordered_map),
then close the browser.

## Week plan

| Day | Work |
|---|---|
| Mon | implement `has_duplicate` and `two_sum_indices`; draw the state after each element |
| Tue | implement `are_anagrams`; compare sorting with frequency counting |
| Wed | implement `deduplicate_sorted`; write its prefix invariant first |
| Thu | implement `max_container_area`; justify every pointer movement |
| Fri | run all tests, add edge cases, update the learning log |
| Sat | solve five problem-pack items and do the measurement task in `EXERCISES.md` |

Build just this week's tests from the module root:

```text
cmake --build --preset default --target cpp_week01_tests
ctest --test-dir build -C Debug -R cpp_week01 --output-on-failure
```

## Checkpoint questions

Answer without notes:

1. Why is `push_back` amortized constant time rather than always constant time?
2. What breaks the usual constant-time claim for a hash map?
3. Which invariant identifies the already-correct prefix in an in-place scan?
4. In the container-area exercise, why can the shorter side be discarded?

