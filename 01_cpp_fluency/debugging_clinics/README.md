# Intentional debugging clinics

These sources are broken on purpose. They are not part of the default build or
CTest suite. Opt in, reproduce one diagnostic, repair one root cause, and rerun
the identical command. A crash, surprising value, or clean unsanitized run does
not identify the language rule that was violated.

## Required diagnostic loop

For each clinic:

1. Read every compiler warning, then record compiler, build configuration,
   exact command, input, and observed symptom before editing. A warning is a
   hypothesis to understand, not noise to suppress.
2. Reproduce under a debugger or the requested sanitizer.
3. Save the diagnostic category and first application-owned stack frame. Do not
   paste pages of runtime internals.
4. State the invalid lifetime, range, or ownership assumption in one causal
   sentence.
5. Make the smallest contract-level repair. Do not disable instrumentation,
   suppress the report, skip the access, or catch a crash signal.
6. Rebuild and rerun the same input and diagnostic configuration.
7. Add a regression check where practical and explain why the repaired lifetime
   or bound now covers every path.

Warnings, debugger observations, and sanitizer reports answer different
questions: warnings are static compiler diagnostics, a debugger exposes one
execution state, and sanitizers instrument executed operations. Final repaired
targets must compile warning-free, but warning-free code is not proof that no
undefined behavior exists.

Use the diagnostic-evidence section in
[WEEKLY_RETROSPECTIVE.md](../progress/WEEKLY_RETROSPECTIVE.md).

## Build routes

From `01_cpp_fluency`, a plain debug build exposes both targets without running
them:

```text
cmake --preset debug-clinics
cmake --build --preset debug-clinics
```

The cross-platform AddressSanitizer route uses a separate build tree:

```text
cmake --preset asan
cmake --build --preset asan
```

On GCC or Clang under Linux/macOS/WSL, run the combined address/undefined route
as a separate configuration:

```text
cmake --preset asan-ubsan
cmake --build --preset asan-ubsan
```

The build output prints each executable path. Visual Studio generators normally
place it under `build/<preset>/RelWithDebInfo/`; single-configuration generators
normally place it directly under `build/<preset>/`. Run one clinic executable at
a time. A nonzero sanitizer exit is expected before repair. Visual Studio
generators copy the matching MSVC sanitizer runtime beside each executable;
other MSVC generators should be run from a Developer PowerShell. A missing-DLL
dialog or immediate exit without a report does not count as reproduction.

Do not combine AddressSanitizer and ThreadSanitizer. The data-race clinic and
Linux/WSL ThreadSanitizer route live with the systems concurrency lab.

## Clinic A: lifetime and a non-owning view

Target: `cpp_lifetime_bug_clinic`

First use a debugger to stop in `make_frame_label` and
`inspect_first_byte`. At each stop record:

- the live owning objects in the selected stack frame;
- the pointer/length held by the view;
- the event after which that pointer no longer denotes a live character; and
- the call stack at the failing read.

Then reproduce with `asan`. The repair must make ownership and borrowing visible
in the function contract; merely changing string length, relying on a library's
small-string optimization, or avoiding the read is not a repair.

## Clinic B: out-of-bounds undefined behavior

Target: `cpp_bounds_bug_clinic`

Run without an argument first, then with indices `0`, `3`, and `4`. In a
debugger, break in `selected_channel`, step over and into calls, inspect `index`
and the local array, and show the caller/callee frames. Reproduce the invalid
case under `asan`; on GCC/Clang also use `asan-ubsan` and compare which tool names
the invalid operation most directly.

The repair must define behavior for every parsed `size_t`, including values far
larger than the array. Record the chosen API policy; do not silently depend on
unchecked `operator[]` becoming checked in a particular build.

## Debugger vocabulary gate

Demonstrate these operations in either Visual Studio, GDB, or LLDB:

- set and remove a source breakpoint;
- continue, step into, step over, and step out;
- inspect arguments and locals;
- select another stack frame and explain the call stack/backtrace; and
- distinguish a debugger observation from a language guarantee.

For the later race clinic, also list threads, select a worker, and inspect each
thread's call stack.

Authoritative tool references:

- Microsoft: [Debug C++ in Visual Studio](https://learn.microsoft.com/en-us/visualstudio/debugger/getting-started-with-the-debugger-cpp?view=visualstudio)
  and [MSVC AddressSanitizer](https://learn.microsoft.com/en-us/cpp/sanitizers/asan?view=msvc-170)
- GDB: [breakpoints and stepping](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Stopping.html),
  [backtraces](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Backtrace.html),
  and [threads](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Threads.html)
- LLVM: [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html),
  [UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html),
  and [ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html)
- GCC: [instrumentation options](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html)
