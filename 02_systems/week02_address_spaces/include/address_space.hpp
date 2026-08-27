#pragma once

#include <cstddef>
#include <cstdint>

namespace systems_course::week02 {

struct AddressSnapshot {
  std::uint64_t process_id = 0;
  std::size_t page_size = 0;
  std::uintptr_t global_object = 0;
  std::uintptr_t stack_object = 0;
  std::uintptr_t heap_object = 0;
};

// Captures the current process ID, native page size, and addresses belonging to
// three different storage-duration/ownership categories. Returned addresses are
// observations for display/comparison only.
AddressSnapshot capture_address_snapshot();

// Writes byte 0xA5 at offsets 0, page_size, 2*page_size, ... within the byte
// range and returns the number of writes. A zero-byte range returns zero and may
// have a null data pointer. A null non-empty range or page_size == 0 throws
// std::invalid_argument.
std::size_t touch_one_byte_per_page(std::byte* data, std::size_t byte_count,
                                    std::size_t page_size);

}  // namespace systems_course::week02
