# Modern C++ engineering exercises

The target is `cpp_owned_buffer_tests`. It is a learner contract and begins red:

```text
cmake --preset default
cmake --build --preset default --target cpp_owned_buffer_tests
ctest --test-dir build -C Debug -R cpp_owned_buffer --output-on-failure
```

## Week 2: ownership and borrowing map

Before implementing the resource owner:

1. Inspect the signatures in Weeks 1-4. Mark each value, reference, raw pointer,
   `optional`, and `string_view` as owner, borrower, or value with no external
   lifetime. For `TreeNode*`, identify which caller must keep nodes alive.
2. Write one example where `const` prevents mutation but does not prevent a
   dangling pointer. Write a separate example where a mutable borrow is safe.
3. Implement `checked_subview`. It returns a borrowed view or the precise
   `SliceError`; it must not add `offset + count` before proving that addition
   cannot overflow.
4. Explain why returning the view does not extend the source lifetime and why an
   empty null view at offset/count zero is valid.
5. Complete both exercises in [the debugging clinic](../debugging_clinics/README.md)
   before reading a proposed repair.

## Week 3: move-only resource owner

Implement the `LEARNER TODO` regions in `starter/owned_buffer.cpp` without
changing the public contract.

Required behavior:

- a default or zero-sized buffer is exactly `{nullptr, 0}`;
- a nonempty buffer owns a dynamically allocated byte array;
- destruction releases that array exactly once;
- copying is rejected at compile time;
- move construction and move assignment transfer the existing allocation
  without copying its bytes or allocating a replacement;
- the source of a move becomes the specified empty state;
- move assignment safely replaces a destination that already owns bytes;
- self-move assignment leaves a valid, destructible representation;
- `data()` and `view()` expose distinct const/non-const borrows; and
- an rvalue owner cannot produce a view through the public interface.

This exercise intentionally uses a raw owning pointer internally. Do not replace
the class with `vector` or `unique_ptr`; compare those Rule-of-Zero designs after
the manual owner passes. Do not add reference counting.

Add at least two tests of your own: one move chain involving an empty buffer and
one scope/container case that would reveal a double release under
AddressSanitizer.

## Week 4: design and safety gate

After all contract tests pass:

1. Run `cpp_owned_buffer_tests` in the `asan` configuration. A normal exit is
   required in addition to green assertions.
2. Sketch the Rule-of-Zero version using `std::unique_ptr<std::byte[]>` or
   `std::vector<std::byte>`. Explain which special members disappear and why.
3. Sketch a real shared-lifetime case and a superficially similar case that
   should use one owner plus borrowers. Draw the control-block cycle in the
   first design and identify the edge that would become `weak_ptr`.
4. For construction, move construction, move assignment, and `checked_subview`,
   state the no-fail/basic/strong exception guarantee that actually follows from
   the operations used. Do not claim a stronger guarantee by intention alone.
5. Explain why a moved-from `OwnedBuffer` has a stronger documented state than
   the generic statement "valid but otherwise unspecified."

The gate is complete when you can implement the owner again from a blank class
declaration and defend every ownership, borrowing, and cleanup edge without
using `shared_ptr` as a blanket lifetime fix.
