# Week 3: Stacks, heaps, and intervals

## Mental models

- A stack remembers the most recent unresolved item. Use it when nesting or a
  "next greater/smaller" relationship makes old items resolvable in reverse.
- A heap exposes the current extreme while accepting new candidates in
  logarithmic time. Ask whether you need all items sorted or only the next best.
- Interval problems usually become local after sorting by a meaningful endpoint.
  State whether intervals are open or closed before deciding if touching means
  overlap.

Read the [`std::priority_queue`](https://en.cppreference.com/w/cpp/container/priority_queue)
reference once. Practice using both the default max heap and a comparator-based
min heap without copying syntax.

## Week plan

| Day | Work |
|---|---|
| Mon | delimiter stack and malformed-input contract |
| Tue | monotonic stack for unresolved temperatures |
| Wed | k-th largest with a bounded heap; compare two heap orientations |
| Thu | sort and sweep closed intervals |
| Fri | edge tests, complexity notes, log update |
| Sat | problem pack plus the stream experiment in `EXERCISES.md` |

## Checkpoint questions

1. What does every element still on your monotonic stack mean?
2. Why can a heap of size `k` be better than sorting all `n` elements?
3. Which sort key makes your interval sweep correct?
4. Does `[1, 4]` overlap `[4, 6]` under this module's contract?

