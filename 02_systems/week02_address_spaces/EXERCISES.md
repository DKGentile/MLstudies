# Week 2 exercises

## Core

1. Implement `capture_address_snapshot` and `touch_one_byte_per_page`.
2. Draw one run's global/static, stack, and heap objects inside a conceptual
   virtual address space. Label the drawing "not to scale; direction is observed."
3. Run the probe for 1, 16, 64, and 256 MiB and log touched-page count plus
   resident/working-set observations.
4. Explain the first-access cost in terms of mapping and page state, without
   claiming every first write necessarily reaches disk.

## Failure injection

- Pass a page size of zero and verify the documented exception.
- Ask for an allocation larger than available memory; record the error path
  without destabilizing the machine. Choose a safe ceiling first.
- Build with AddressSanitizer on a supported toolchain and temporarily write one
  byte past the buffer. Save the diagnostic summary, then revert the bug.

## Stretch

Add a separate, platform-specific `resident_bytes()` measurement. Keep it out of
the portable snapshot contract. Compare it with virtual size before and after
touching and explain why tools may sample at different times.

