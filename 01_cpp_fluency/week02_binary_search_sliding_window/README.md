# Week 2: Binary search and sliding windows

## Mental models

Binary search is not "look at the middle." It finds a boundary in an ordered
range or a monotonic truth sequence. Before typing, complete this sentence:
"For every candidate after the boundary, the predicate is _____."

A sliding window maintains a claim about one contiguous range. Expansion adds
information; contraction restores the invariant or makes the range minimal.
Write down what enters, what leaves, and why neither boundary must move backward.

The window's iterators, references, and views borrow storage. An index being in
range does not keep the indexed container alive; state both the range invariant
and the lifetime owner.

## Prepare

Required reading, about 25-35 minutes total:

- Read Cornell CS 2112's
  [binary-search loop invariant](https://www.cs.cornell.edu/courses/cs2112/2018fa/lectures/lec_loopinv/).
  Focus on the represented interval, preservation after either boundary update,
  and the strictly decreasing termination measure.
- Read Microsoft's [`lower_bound` contract](https://learn.microsoft.com/en-us/cpp/standard-library/algorithm-functions?view=msvc-170#lower_bound).
  Identify its sorted-range precondition, half-open iterator range, return value,
  and complexity qualification for different iterator categories.
- Read the official statements and built-in hints for
  [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/),
  [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/),
  and [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/).
  Before opening a hint, write the monotonic predicate or the exact state owned by
  the current window.

Optional video: [MIT 6.0001 Lecture 12: Searching and Sorting](https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/resources/lecture-12-searching-and-sorting/),
using the bisection-search portion for a second explanation.

**Required Modern C++ thread, spread across the week:** read the Week 2 row and
language model in [Modern C++ engineering](../modern_cpp_engineering/README.md).
Classify automatic versus dynamic lifetime, values versus references/raw
pointers, ownership versus borrowing, and const access. Then implement the
`variant`-based checked subview and complete the two opt-in
[debugging clinics](../debugging_clinics/README.md). This replaces one practice
problem and the optional video unless the algorithm explanation is still needed.

Before coding, verify that you can:

- label every part of your chosen search interval as known or still possible;
- state a Boolean predicate and prove that it changes truth value at most once;
- name the state added and removed at each window boundary; and
- explain which input property permits each boundary to move only forward;
- name the owner behind a `string_view` or raw pointer and the event that would
  invalidate the borrow; and
- explain why `const` access neither owns nor extends a lifetime.

## Week plan

| Day | Work |
|---|---|
| Mon | implement `first_not_less_than`; trace empty, all-false, and all-true predicates |
| Tue | implement rotated search and minimum feasible eating speed |
| Wed | implement minimum positive-sum window and state why positivity matters |
| Thu | implement longest unique byte span with a frequency map or last-seen table |
| Fri | add boundary tests; implement checked borrowed slicing; log off-by-one mistakes |
| Sat | four-item problem pack, recall/instrumentation, then lifetime and bounds clinics |

## Required checkpoint

For each binary search, identify:

- the half-open or closed interval represented by your variables;
- the monotonic predicate;
- whether the final value is known-valid, known-invalid, or a sentinel;
- why the loop strictly shrinks.

For each window, identify the exact state updated when the left boundary moves.
For each borrowed range, identify the owner and prove that it outlives every
access. Given one clinic diagnostic, name its first application frame and the
violated lifetime or range rule before proposing a repair.
