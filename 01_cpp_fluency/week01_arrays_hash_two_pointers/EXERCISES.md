# Week 1 exercises

## A. Contract implementation

Implement every `TODO` in `starter/week01.cpp`. Do not change a signature or
weaken a test. Add at least one test for each of these cases:

- an empty input;
- duplicate negative values;
- two-sum values whose indices are far apart;
- repeated values in a sorted vector;
- very tall container lines whose product exceeds a 32-bit signed integer.

Write the expected time and auxiliary space above each function before coding.

## B. Representation experiment

Create a temporary benchmark (do not optimize the course tests) that inserts
and queries at least 100,000 integers in both a `std::vector` and an
`std::unordered_set`. Measure construction and lookup separately with
`std::chrono::steady_clock`. Record:

- compiler and optimization level;
- input size and hit/miss ratio;
- elapsed time for each operation;
- why the faster result does not mean one container is universally better.

Numbers belong in your weekly retrospective.

## C. Problem pack

Use the public problem statements on LeetCode: 1, 217, 242, 49, 167, 15, 3,
and 11. Complete at least five, with the first two easy and at least two medium.
Log each independent attempt. If one is already automatic, substitute the next
array/hash/two-pointer item from the NeetCode roadmap.

## D. Recall gate

The next morning, in a blank file, implement duplicate detection and in-place
deduplication in 20 minutes. No snippets, autocomplete-generated bodies, or
notes. Compile with warnings enabled.

