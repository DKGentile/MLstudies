# Modern C++ engineering: ownership, lifetime, and value semantics

This is a required thread through C++ Weeks 2-4, not a fifth week. The
algorithm exercises build fluency; this supplement makes the ownership rules
needed by later process, thread, CUDA, and TensorRT code explicit.

## The model to carry forward

- **Storage duration is a language lifetime category.** Automatic objects are
  normally implemented with a call stack and dynamic allocations normally come
  from a heap, but "stack" and "heap" are useful implementation models rather
  than interchangeable names for the standard's lifetime rules.
- A value or owning object controls a resource lifetime. A reference, raw
  pointer, `std::string_view`, or this lab's byte view normally **borrows**; it
  does not keep the referred object alive. `const` controls permitted mutation,
  not lifetime and not ownership.
- RAII binds acquisition to an object's invariant and release to deterministic
  destruction. Every return and exception path then crosses the same
  destructor boundary.
- Prefer values and the Rule of Zero. Use `std::unique_ptr` when ownership must
  live behind a pointer. Use `std::shared_ptr` only when multiple independent
  owners genuinely determine the lifetime; its control block and atomic
  reference counts are not free. A `std::weak_ptr` observes without owning and
  can break a shared-ownership cycle.
- `std::move` does not move anything by itself. It permits move-aware overload
  resolution. The selected constructor or assignment operation performs the
  transfer. A moved-from object remains valid and destructible, but only the
  type's contract tells you which other operations have useful results.
- `std::optional<T>` represents zero-or-one `T`. `std::variant<A, B>` represents
  exactly one named alternative. Neither type implies dynamic allocation or
  shared ownership.
- A non-owning view is safe only while its source storage remains alive and
  stable. Returning a `std::string_view` into a local string, retaining a view
  across owner destruction, or retaining one across an invalidating
  reallocation creates a dangling view.

## Three-week route

| Course week | Required focus | Implementation evidence |
|---|---|---|
| 2 | automatic/dynamic lifetime; references; raw pointers; `const`; ownership vs borrowing; `optional`, `variant`, and `string_view` | classify existing APIs, implement checked borrowed slicing, and complete the lifetime/bounds debugging clinics |
| 3 | RAII; deterministic destruction; `unique_ptr`; deliberate shared ownership; `weak_ptr` and cycles; copy/move operations | implement allocation, release, and ownership transfer for `OwnedBuffer` |
| 4 | Rule of Zero/Five; value semantics; moved-from contracts; exception/resource safety | finish awkward move/view cases and pass the ownership explanation gate |

## Prepare at the point of use

Use the linked sections, not each entire reference:

- C++ Core Guidelines [R.1-R.5 and R.20-R.24](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-resource)
  for resource handles, owning versus non-owning pointers/references, and smart
  pointer choice.
- cppreference on the [Rule of Three/Five/Zero](https://en.cppreference.com/w/cpp/language/rule_of_three)
  and [move constructors](https://en.cppreference.com/w/cpp/language/move_constructor)
  for special-member generation and moved-from state.
- cppreference on [`std::unique_ptr`](https://en.cppreference.com/w/cpp/memory/unique_ptr),
  [`std::shared_ptr`](https://en.cppreference.com/w/cpp/memory/shared_ptr), and
  [`std::weak_ptr`](https://en.cppreference.com/w/cpp/memory/weak_ptr). State
  who decides the destruction time before choosing among them.
- cppreference on [`std::optional`](https://en.cppreference.com/w/cpp/utility/optional),
  [`std::variant`](https://en.cppreference.com/w/cpp/utility/variant), and
  [`std::string_view`](https://en.cppreference.com/w/cpp/string/basic_string_view).
  For every view example, name the owner and the invalidation event.
- C++ Core Guidelines [E.6](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#e6-use-raii-to-prevent-leaks)
  for exception-safe cleanup. This lab requires the basic guarantee (valid
  invariants and no leaks) and identifies where operations provide the stronger
  no-fail guarantee.

## Ready-to-code checks

Answer without the source open:

1. Which object owns the bytes, and which APIs merely borrow them?
2. Why does `const std::byte*` say nothing about who releases the allocation?
3. Which special members would a raw owning pointer get by default, and why are
   those operations wrong for unique ownership?
4. What exactly must a move operation change in the source so both destructors
   remain safe?
5. Why is `std::shared_ptr` inappropriate when one lexical owner can outlive all
   borrowers? How can a two-node ownership cycle prevent both destructors?
6. Why can a valid `std::string_view` become invalid without the view object
   itself changing?
7. If allocation throws during construction, which resources already exist and
   which destructor calls are guaranteed?

Then follow the contracts in [EXERCISES.md](EXERCISES.md). Build details and
sanitizer routes are in [BUILDING.md](../BUILDING.md).

## Why one manual owner exists here

Ordinary byte storage should usually be a `std::vector<std::byte>` or
`std::unique_ptr<std::byte[]>`. `OwnedBuffer` intentionally manages one raw
handle so you must implement the ownership transfer yourself. Later wrappers
around OS handles, CUDA allocations, streams, and inference objects have the
same shape even when their acquire/release functions are not `new[]` and
`delete[]`. Do not generalize this exercise into a custom container library.
