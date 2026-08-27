# Week 2: Binary search and sliding windows

## Mental models

Binary search is not "look at the middle." It finds a boundary in an ordered
range or a monotonic truth sequence. Before typing, complete this sentence:
"For every candidate after the boundary, the predicate is _____."

A sliding window maintains a claim about one contiguous range. Expansion adds
information; contraction restores the invariant or makes the range minimal.
Write down what enters, what leaves, and why neither boundary must move backward.

## Week plan

| Day | Work |
|---|---|
| Mon | implement `first_not_less_than`; trace empty, all-false, and all-true predicates |
| Tue | implement rotated search and minimum feasible eating speed |
| Wed | implement minimum positive-sum window and state why positivity matters |
| Thu | implement longest unique byte span with a frequency map or last-seen table |
| Fri | add boundary tests and log off-by-one mistakes |
| Sat | problem pack, recall drill, and predicate instrumentation |

## Required checkpoint

For each binary search, identify:

- the half-open or closed interval represented by your variables;
- the monotonic predicate;
- whether the final value is known-valid, known-invalid, or a sentinel;
- why the loop strictly shrinks.

For each window, identify the exact state updated when the left boundary moves.

