# Week 3: Stacks, heaps, and intervals

## Mental models

- A stack remembers the most recent unresolved item. Use it when nesting or a
  "next greater/smaller" relationship makes old items resolvable in reverse.
- A heap exposes the current extreme while accepting new candidates in
  logarithmic time. Ask whether you need all items sorted or only the next best.
  This heap data structure is unrelated to using "the heap" as shorthand for a
  process's dynamic-allocation region.
- Interval problems usually become local after sorting by a meaningful endpoint.
  State whether intervals are open or closed before deciding if touching means
  overlap.

## Prepare

Required reading, about 25-35 minutes total:

- Read Cornell CS 2110's [Stacks and Queues](https://www.cs.cornell.edu/courses/cs2110/2025fa/lectures/lec15/)
  through the LIFO/FIFO abstractions, then Microsoft's
  [`std::stack` reference](https://learn.microsoft.com/en-us/cpp/standard-library/stack-class?view=msvc-170).
  Connect restricted access to the meaning of an unresolved item at the top.
- Read Microsoft's
  [`std::priority_queue` reference](https://learn.microsoft.com/en-us/cpp/standard-library/priority-queue-class?view=msvc-170).
  Focus on `top`, comparator orientation, and the costs of access, insertion, and
  removal. Practice declaring a min-oriented queue without copying an answer.
- Read the official statements and built-in hints for
  [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) and
  [Merge Intervals](https://leetcode.com/problems/merge-intervals/).
  Write what remains unresolved on the stack, then specify the interval endpoint
  convention and a sort key before opening a hint.

Optional video: [MIT 6.006 Lecture 4: Heaps and Heap Sort](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/lecture-4-heaps-and-heap-sort/).

**Required Modern C++ thread:** complete the Week 3 route in
[Modern C++ engineering](../modern_cpp_engineering/README.md). Read the focused
RAII and smart-pointer rules, then implement the allocation, destruction, and
move operations for `OwnedBuffer`. Before typing each special member, draw the
source and destination `{pointer, size}` state before and after it. The exercise
replaces one problem-pack item; the million-element comparison becomes an
after-first-attempt extension.

Before coding, verify that you can:

- state what every item remaining on a stack is waiting for;
- choose which extreme belongs at a heap root and maintain a size-`k` invariant;
- justify why retaining only `k` candidates can beat sorting all `n`; and
- state the interval endpoint convention, overlap rule, and sort key that makes
  a one-pass sweep valid;
- distinguish raw ownership from a raw borrow and state the destructor that
  closes every successful acquisition path; and
- explain why `std::move` alone neither transfers nor destroys a resource.

## Week plan

| Day | Work |
|---|---|
| Mon | delimiter stack and malformed-input contract |
| Tue | monotonic stack for unresolved temperatures |
| Wed | k-th largest with a bounded heap; compare two heap orientations |
| Thu | sort and sweep closed intervals |
| Fri | edge tests, then `OwnedBuffer` allocation/destruction and copy deletion |
| Sat | move/view tests, four-item problem pack, and the optional stream experiment if time remains |

## Checkpoint questions

1. What does every element still on your monotonic stack mean?
2. Why can a heap of size `k` be better than sorting all `n` elements?
3. Which sort key makes your interval sweep correct?
4. Does `[1, 4]` overlap `[4, 6]` under this module's contract?
5. After move construction, which object owns the allocation and which exact
   state makes the source destructor safe?
6. When is shared ownership necessary, and why is `shared_ptr` not a default
   substitute for reasoning about one owner and its borrowers?
