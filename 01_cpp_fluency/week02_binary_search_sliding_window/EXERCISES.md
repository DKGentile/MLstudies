# Week 2 exercises

## A. Contract implementation

Implement all `TODO`s in `starter/week02.cpp`. Write the loop invariant above
each binary search and the maintained window state above each sliding-window
function. Your production functions must not print.

Add tests for integer extremes, a one-element rotated array, repeated bytes in a
string, and a target met by exactly one array element.

## B. Make logarithmic work visible

Temporarily instrument `first_not_less_than` with a predicate-evaluation count.
Run it on sorted inputs of size 1, 10, 100, 1,000, and 1,000,000. Record the
worst count and compare it with a linear scan. Remove the instrumentation from
the submitted function but keep the table in your retrospective.

## C. Ownership, views, and diagnostics

Complete the Week 2 section of
[`modern_cpp_engineering/EXERCISES.md`](../modern_cpp_engineering/EXERCISES.md):

- classify the module's owners and borrowers;
- implement and test `checked_subview` without unsigned overflow; and
- reproduce, repair, and rerun both intentional C++ bug clinics.

For each diagnostic, record the compiler/tool version, exact command, report
category, first application frame, root cause, repair, and clean rerun.

## D. Problem pack

Use LeetCode 704, 35, 33, 153, 875, 209, and 76. Complete four; attempt 76 only
after the other window invariants are solid. The ownership/debugging work
replaces one item of duplicate practice volume. Log the predicate or window
state before starting each attempt.

## E. Recall gate

The next morning, write a generic "first true" binary search over an integer
domain and a minimum-length positive-sum window in a blank file. Use a tiny
assert-based harness you write yourself.
