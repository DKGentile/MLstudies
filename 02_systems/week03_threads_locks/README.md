# Week 3 lab: Threads, locks, and condition variables

## Prepare

**Required concepts**

- Read OSTEP Chapters [26: Concurrency--An
  Introduction](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-intro.pdf), [27:
  Thread API](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-api.pdf), [28:
  Locks](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-locks.pdf), [29:
  Lock-Based Concurrent Data
  Structures](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-locks-usage.pdf),
  and **[30: Condition
  Variables](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-cv.pdf)**. Chapter 30
  is required: it supplies the wait-condition model used by this lab.
- Read C++ Core Guidelines [CP.42: do not wait without a
  condition](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#cp42-dont-wait-without-a-condition).
  For capacity 1, draw the queue state, each wait predicate, and every state
  transition that can make a predicate true. "It usually runs in this order" is
  not a synchronization argument.

**API references while coding**

- Microsoft's [`<condition_variable>`
  reference](https://learn.microsoft.com/en-us/cpp/standard-library/condition-variable?view=msvc-170)
  is the readable API guide. Use the C++ working draft for authoritative
  [condition-variable ordering](https://eel.is/c++draft/thread.condition) and
  [happens-before/data-race rules](https://eel.is/c++draft/intro.races).

**Optional / after the first attempt**

- Watch CppCon's [Back to Basics: C++
  Concurrency](https://www.youtube.com/watch?v=8rEGu20Uw4g) if you want a second
  treatment of races, mutexes, and atomics before the recall drill.
- After the ordinary tests pass, use Clang's [ThreadSanitizer
  guide](https://clang.llvm.org/docs/ThreadSanitizer.html) for Experiment 5.
  Record the exercised workload: a clean run is evidence about those executions,
  not a proof that no race exists.

## Build target

Implement the generic bounded queue in `starter/bounded_queue.hpp`:

- capacity is fixed and nonzero;
- `push` blocks while full, then inserts, unless closure makes it return false;
- `pop` blocks while empty, then removes FIFO, unless closed-and-empty makes it
  return `std::nullopt`;
- `close` is idempotent and wakes every blocked producer and consumer;
- every shared state read/write is synchronized.

Use the provided mutex, condition variables, and deque. Guard waits with
predicates because wakeups can be spurious and because another thread can win
the mutex before the woken thread reacquires it. Change state while holding the
mutex, then notify the side whose predicate may have become true.

`systems_week03_tests` has a 10-second outer timeout so a deadlock becomes an
explicit failure rather than an endless run.

## Experiments

1. Capacity 1: draw producer and consumer states for every operation.
2. Four producers, two consumers, 100,000 integer IDs: verify every ID is seen
   exactly once with a local set/bitmap in the test harness.
3. Compare capacities 1, 8, 64, and 1024. Record elapsed time and max observed
   queue occupancy (temporary instrumentation is allowed).
4. Remove a wait predicate, run repeatedly, and explain any failure or why the
   bug remains possible even when not observed. Restore it.
5. Run ThreadSanitizer on Linux/Clang or GCC if available. Record tool/version
   and result; do not claim absence of a reported race proves correctness.

## ML systems connection

A capture thread can outpace inference. Bounded queues make backpressure and
memory use explicit. Write a policy note comparing: block capture, drop newest,
drop oldest, or sample. The generic queue implements blocking; the policy note
explains when an embedded perception pipeline might choose differently.

## Done when

- all queue tests pass repeatedly;
- close unblocks both kinds of waiter and queued items drain before end-of-stream;
- you can point to the invariant protected by the mutex;
- you can explain why checking `empty()` and later calling `pop()` under separate
  locks would be a time-of-check/time-of-use bug.
