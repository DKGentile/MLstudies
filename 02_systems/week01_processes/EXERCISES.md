# Week 1 exercises

## Core

1. Implement `run_process` for your primary OS.
2. Add a test where the child echoes an empty argument and a Unicode argument.
3. Add a child mode that prints its PID and parent PID; diagram the relationship.
4. Force a nonexistent executable and define a deliberate error contract. Add a
   regression test without weakening the existing API behavior.

## Failure injection

Choose two and record the result:

- child exits nonzero after writing both streams;
- parent closes its read end early;
- child writes enough output to fill a pipe;
- one handle/descriptor is intentionally left open;
- child is terminated before normal exit.

Restore the correct implementation after every injection.

## Stretch

Add an overload with a deadline and a result flag for timeout. Specify what
happens to the child and descendants on timeout before implementing it. Avoid
silently leaving an orphan worker.

