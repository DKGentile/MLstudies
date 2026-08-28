# Week 2 lab: Address spaces, allocation, and resident pages

## Prepare

**Required concepts**

- Read OSTEP [Chapter 13: The Address
  Space](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-intro.pdf), [Chapter 14:
  Memory API](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-api.pdf), and [Chapter
  15: Address
  Translation](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-mechanism.pdf). Be able
  to distinguish virtual address, physical memory, mapping, translation, and a
  page fault before implementing the probe.
- Read Microsoft's [virtual-address-space
  overview](https://learn.microsoft.com/en-us/windows/win32/memory/virtual-address-space)
  and [working-set
  guide](https://learn.microsoft.com/en-us/windows/win32/memory/working-set).
  Before Experiments 2-3, predict which quantities allocation can change and
  which require touching pages. Do not infer physical layout from the numeric
  order of virtual addresses.

**API references while coding**

- Windows: the [`VirtualAlloc` reserve/commit
  model](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc)
  and Microsoft's [`GetSystemInfo`
  example](https://learn.microsoft.com/en-us/windows/win32/sysinfo/getting-hardware-information).
  The probe need not call `VirtualAlloc`; use its documentation to interpret
  reserve, commit, and first-touch observations rather than treating them as
  synonyms.

**Optional / after the first attempt**

- Inspect a completed allocate/touch run with [VMMap's official
  documentation](https://learn.microsoft.com/en-us/sysinternals/downloads/vmmap)
  and [video
  walkthrough](https://learn.microsoft.com/en-us/shows/defrag-tools/7-vmmap).
  Reconcile its reserved, committed, and working-set values with your prediction
  instead of replacing your measurements with screenshots.

## Build target

Implement these contracts in `starter/address_space.cpp`:

- process ID and OS page-size discovery;
- a snapshot containing addresses of global/static, stack, and heap objects;
- one-byte-per-page touching for a `(pointer, byte count)` buffer view.

Use `GetCurrentProcessId` and `GetSystemInfo` on Windows, or `getpid` and
`sysconf(_SC_PAGESIZE)` on POSIX. Object addresses can be converted to
`std::uintptr_t` for display; never dereference a reconstructed integer address.

After the contract test passes, build and run:

```text
systems_address_probe 256 10000
```

The first argument allocates MiB, and the optional second argument keeps the
process alive in milliseconds so you can inspect it. The driver is provided;
your address/page functions supply its observations.

## Experiments

For each, predict first and log the numbers:

1. Run the probe three times. Which numeric addresses change because of ASLR?
2. Compare 1, 64, and 256 MiB. Observe working set/resident set while the process
   is held. On Windows use Task Manager, Resource Monitor, or Process Explorer;
   on Linux use `ps`, `pmap`, `/proc/<pid>/maps`, and `/proc/<pid>/smaps_rollup`.
3. Temporarily allocate without calling `touch_one_byte_per_page`. Compare
   committed/resident memory, then restore the call. The provided probe uses a
   default-initialized byte array specifically to avoid a container constructor
   value-initializing every byte before your explicit page touches.
4. Build Debug and Release. Which addresses or sizes are stable guarantees, and
   which are merely observations?
5. Change the touch stride to twice the page size. Predict the touched count and
   resident-memory direction.

## ML systems connection

A tensor's logical shape does not by itself tell you which pages are resident or
whether access is sequential. Explain why touching every page, batching adjacent
elements, and reusing a working set can affect latency even before a GPU kernel
runs.

## Done when

- `systems_week02_tests` passes.
- Your implementation has both Windows and POSIX branches, or explicitly logs
  the unimplemented secondary platform.
- Your report separates address-space observations from portability guarantees.
- You can explain why "I allocated N MiB" need not mean N MiB became resident at
  the same instant.
