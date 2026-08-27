# C++ Fluency: Phase 0

This is a four-week, code-first reset for the C++ patterns used later in ML,
computer vision, and systems work. The target is not to memorize interview
tricks. It is to make common data structures, invariants, and debugging habits
automatic enough that they no longer consume attention during harder work.

## How to use this module

Budget 60-75 minutes Monday through Thursday, 45 minutes Friday, and one
three-hour block on Saturday.

1. Read the week's `README.md` for no more than 20 minutes.
2. Open the public API in `include/`, then implement only the `TODO`s in
   `starter/`.
3. Build and run that week's test executable after every small change.
4. Solve five of the linked practice problems without copying a solution.
5. The next morning, use `progress/RECALL_DRILL.md` and rebuild the core idea
   in a blank file from memory.
6. Record attempts and failures in `progress/learning_log.csv`.

The checked-in starter code is intentionally incomplete. It should compile,
but its tests initially fail with `TODO` errors. That is the starting line,
not a broken repository.

## Four-week map

| Week | Pattern | You are done when... |
|---|---|---|
| 1 | arrays, hash maps, two pointers | you can choose between indexing, counting, and paired scans and state the complexity |
| 2 | binary search, sliding window | you can name the monotonic predicate or window invariant before typing |
| 3 | stacks, heaps, intervals | you can explain why the next item to process lives at one end, at the heap root, or in sorted order |
| 4 | trees, BFS/DFS, union-find, topological sort | you can select the traversal/state model from the problem's question |

## Build and test

You need a C++17 compiler and CMake 3.21 or newer. From this directory:

```bash
cmake --preset default
cmake --build --preset default
ctest --preset default
```

Or run `powershell -ExecutionPolicy Bypass -File scripts/run_checks.ps1` on a
Windows host whose local policy blocks scripts, and
`sh scripts/run_checks.sh` in a POSIX shell. To focus on one week:

```bash
ctest --test-dir build -R cpp_week02 --output-on-failure
```

See `BUILDING.md` for compiler setup and direct compiler commands. Never add
the `build/` directory to your learning log or solution commits.

## Rules that preserve learning value

- Do not edit the tests merely to make red output green. If you believe a
  contract is wrong, write the disagreement in the weekly retrospective first.
- Prefer a small correct implementation, then measure. Avoid clever one-liners.
- Before coding, write the invariant in a comment. Delete the comment only if
  the code expresses it more clearly.
- Treat invalid-input behavior in the headers as part of the API.
- After week 2, use tooling as a reviewer: ask for counterexamples or complexity
  critique, not an implementation.

## Exit check

Phase 0 C++ fluency is complete when you can implement BFS and union-find from
memory, pass every contract test, solve four medium problems in one sitting,
and explain the time and auxiliary-space cost of every function in this module.
