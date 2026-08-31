#include "owned_buffer.hpp"

#include <stdexcept>

namespace cpp_course::modern_cpp {

ConstSliceResult checked_subview(ConstByteView source, std::size_t offset,
                                 std::size_t count) noexcept {
  (void)source;
  (void)offset;
  (void)count;
  // LEARNER TODO: Validate without unsigned overflow and return either a
  // borrowed subview or the precise SliceError.
  return SliceError::offset_out_of_range;
}

OwnedBuffer::OwnedBuffer(std::size_t size) {
  (void)size;
  // LEARNER TODO: Establish the class invariant for zero and nonzero sizes.
  throw std::logic_error("TODO: implement OwnedBuffer allocation");
}

OwnedBuffer::~OwnedBuffer() {
  // LEARNER TODO: Release the owned byte array exactly once.
}

OwnedBuffer::OwnedBuffer(OwnedBuffer&& other) noexcept {
  (void)other;
  // LEARNER TODO: Transfer ownership and leave other in its specified empty
  // state. No allocation or other throwing operation belongs here.
}

OwnedBuffer& OwnedBuffer::operator=(OwnedBuffer&& other) noexcept {
  (void)other;
  // LEARNER TODO: Handle the destination's current resource, ownership
  // transfer, the moved-from invariant, and self-move safely.
  return *this;
}

ByteView OwnedBuffer::view() & noexcept {
  // LEARNER TODO: Return a non-owning mutable view of this live buffer.
  return {};
}

ConstByteView OwnedBuffer::view() const& noexcept {
  // LEARNER TODO: Return a non-owning read-only view of this live buffer.
  return {};
}

}  // namespace cpp_course::modern_cpp
