# Week 1: Arrays, hashing, and two pointers

## Mental models

- A `std::vector` stores elements contiguously: indexing is constant time and
  sequential scans are cache-friendly. Inserting at the front is not free.
- A hash table trades ordering and some memory for average constant-time key
  lookup. Correctness cannot depend on iteration order.
- Two pointers are useful when progress at one boundary lets you discard work
  at the other. State the reason a pointer move is safe.

## Prepare

Required reading, about 35-45 minutes total:

- Read the dynamic-array and amortized-analysis portions of
  [MIT 6.006 Lecture 2 notes](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/79a07dc1cb47d76dae2ffedc701e3d2b_MIT6_006S20_lec2.pdf),
  then inspect `capacity`, `reserve`, reallocation, and iterator invalidation in
  Microsoft's [`std::vector` reference](https://learn.microsoft.com/en-us/cpp/standard-library/vector-class?view=msvc-170).
  These distinguish one expensive growth operation from the amortized cost of a
  sequence of appends.
- Use [MIT 6.006 Lecture 4: Hashing](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-4-hashing/)
  for collision handling and expected versus worst-case analysis, then inspect
  buckets, load factor, and rehashing in Microsoft's
  [`std::unordered_map` reference](https://learn.microsoft.com/en-us/cpp/standard-library/unordered-map-class?view=msvc-170).
- Read Cornell CS 2110's
  [loop-invariant proof obligations](https://www.cs.cornell.edu/courses/cs2110/2025fa/lectures/lec04/):
  initialization, preservation, postcondition, and termination. Apply its array
  segment notation to an already-correct output prefix.
- Read the official statements for
  [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)
  and [Container With Most Water](https://leetcode.com/problems/container-with-most-water/).
  Use the built-in hints only after writing your own prefix invariant and an
  upper-bound argument for every pair that retains the shorter endpoint.

Optional video: [MIT 6.006 Lecture 2: Data Structures and Dynamic Arrays](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-2-data-structures-and-dynamic-arrays/).

Before coding, verify that you can:

- distinguish worst-case cost for one append from amortized cost over many appends;
- state when hash-table operations are expected constant time and construct the
  bucket distribution that makes them linear;
- write a prefix invariant with initialization, preservation, and exit meaning; and
- write the inequality that rules out every narrower container retaining the
  current shorter side.

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
