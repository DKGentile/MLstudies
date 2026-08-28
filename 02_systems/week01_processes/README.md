# Week 1 lab: Processes are isolated resource containers

## Prepare

**Required concepts**

- Read OSTEP [Chapter 4: The Abstraction--The
  Process](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf) and
  [Chapter 5: Process
  API](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-api.pdf). Before coding, draw
  parent and child state across create, replace/exec, exit, and wait. Label the
  owner of each address space and OS resource.
- Read Microsoft's [redirected child-I/O
  walkthrough](https://learn.microsoft.com/en-us/windows/win32/procthread/creating-a-child-process-with-redirected-input-and-output),
  [anonymous-pipe
  operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations),
  and [pipe-handle
  inheritance](https://learn.microsoft.com/en-us/windows/win32/ipc/pipe-handle-inheritance).
  Predict what Experiment 5 does if either pipe fills or the parent retains an
  extra child-side write handle.

**API references while coding**

- Windows: [creating
  processes](https://learn.microsoft.com/en-us/windows/win32/procthread/creating-processes),
  [`CreateProcessW`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw),
  [`WaitForSingleObject`](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject),
  and [MSVC command-line argument
  rules](https://learn.microsoft.com/en-us/cpp/cpp/main-function-command-line-args?view=msvc-170).
  Use these to check ownership, wait/status behavior, and exact argument
  boundaries; do not copy the walkthrough as a finished runner.

**Optional / after the first attempt**

- Use the official [Task Manager and Resource Monitor
  walkthrough](https://learn.microsoft.com/en-us/shows/defrag-tools/12-taskmgr-resmon)
  before Experiments 3-4 if the Windows process-state views are unfamiliar.

## Build target

Implement `run_process` in `starter/process_runner.cpp` on your current OS. It
must launch an executable directly, preserve argument boundaries, capture stdout
and stderr separately, wait for termination, and return its exit code.

- Windows path: anonymous pipes, inheritable child handles, `CreateProcessW`,
  `WaitForSingleObject`, `GetExitCodeProcess`, and complete handle cleanup.
- POSIX path: `pipe`, `fork`, `dup2`, `execv`/`execvp`, `waitpid`, and complete
  file-descriptor cleanup.

Do not concatenate a shell command. Argument quoting/encoding is part of the
Windows branch; `argv` construction is part of the POSIX branch. Drain both
output pipes without creating a full-pipe deadlock.

The test supplies `probe/child_probe.cpp` as the known child. It checks only
observable behavior, not which platform calls you chose.

## Experiments

1. Put a breakpoint immediately after child creation. Draw which handles or file
   descriptors exist in parent and child.
2. Run the probe with exits 0, 7, and 42. Record parent PID, child PID (add
   temporary instrumentation), and status.
3. Make the child sleep for five seconds. Observe it in Task Manager/Process
   Explorer on Windows or `ps -o pid,ppid,state,cmd` on Linux.
4. Temporarily skip the wait. Observe what changes, then restore correct code.
5. Ask the child to emit more than a pipe buffer to stdout and stderr. If it
   hangs, explain the dependency cycle before changing code.

## ML systems connection

Inference supervisors often isolate workers because a process owns a separate
address space and failure boundary. Write three sentences comparing a child
process worker with an in-process thread worker: startup cost, memory sharing,
and failure containment.

## Done when

- `systems_week01_tests` passes on one OS.
- Every acquired OS resource has an explicit owner and cleanup path.
- An argument containing spaces and shell punctuation arrives as one argument.
- You can explain the difference between creating a process and replacing its
  program image.
