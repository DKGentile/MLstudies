#pragma once

#include <cstddef>
#include <variant>

namespace cpp_course::modern_cpp {

// These views borrow bytes. They never destroy the memory and must not outlive
// the object that owns it. A nonzero size requires data to point to at least
// that many live bytes; constructing a view that violates this is caller error.
struct ByteView {
  std::byte* data = nullptr;
  std::size_t size = 0;
};

struct ConstByteView {
  const std::byte* data = nullptr;
  std::size_t size = 0;
};

enum class SliceError {
  offset_out_of_range,
  length_out_of_range,
};

using ConstSliceResult = std::variant<ConstByteView, SliceError>;

// Returns a borrowed subview when [offset, offset + count) is within source.
// An offset equal to source.size is valid only when count is zero. The
// implementation must reject ranges without overflowing size_t arithmetic.
ConstSliceResult checked_subview(ConstByteView source, std::size_t offset,
                                 std::size_t count) noexcept;

// A deliberately small RAII exercise that resembles a future OS/GPU resource
// wrapper. OwnedBuffer uniquely owns a dynamic byte array. A zero-sized or
// moved-from buffer is represented by {nullptr, 0}.
class OwnedBuffer {
 public:
  OwnedBuffer() noexcept = default;
  explicit OwnedBuffer(std::size_t size);
  ~OwnedBuffer();

  OwnedBuffer(const OwnedBuffer&) = delete;
  OwnedBuffer& operator=(const OwnedBuffer&) = delete;

  OwnedBuffer(OwnedBuffer&& other) noexcept;
  OwnedBuffer& operator=(OwnedBuffer&& other) noexcept;

  std::size_t size() const noexcept { return size_; }
  bool empty() const noexcept { return size_ == 0; }

  std::byte* data() noexcept { return data_; }
  const std::byte* data() const noexcept { return data_; }

  ByteView view() & noexcept;
  ConstByteView view() const& noexcept;
  ByteView view() && = delete;
  ConstByteView view() const&& = delete;

 private:
  std::byte* data_ = nullptr;
  std::size_t size_ = 0;
};

}  // namespace cpp_course::modern_cpp
