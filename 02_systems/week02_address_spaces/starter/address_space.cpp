#include "address_space.hpp"

#include <stdexcept>

namespace systems_course::week02 {

AddressSnapshot capture_address_snapshot() {
  // TODO: Use small, live objects for the address categories. Put OS-specific
  // process/page queries behind _WIN32 and POSIX conditional compilation.
  throw std::logic_error("TODO: implement capture_address_snapshot");
}

std::size_t touch_one_byte_per_page(std::byte* data, std::size_t byte_count,
                                    std::size_t page_size) {
  (void)data;
  (void)byte_count;
  (void)page_size;
  throw std::logic_error("TODO: implement touch_one_byte_per_page");
}

}  // namespace systems_course::week02
