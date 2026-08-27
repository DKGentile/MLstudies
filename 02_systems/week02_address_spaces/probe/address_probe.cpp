#include "address_space.hpp"

#include <chrono>
#include <cstddef>
#include <exception>
#include <iostream>
#include <limits>
#include <memory>
#include <stdexcept>
#include <string>
#include <thread>

namespace {

std::size_t parse_nonnegative(const char* text, const char* label) {
  const unsigned long long parsed = std::stoull(text);
  if (parsed > std::numeric_limits<std::size_t>::max()) {
    throw std::out_of_range(std::string(label) + " is too large");
  }
  return static_cast<std::size_t>(parsed);
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc < 2 || argc > 3) {
      std::cerr << "usage: systems_address_probe MIB [HOLD_MILLISECONDS]\n";
      return 64;
    }

    constexpr std::size_t bytes_per_mib = 1024U * 1024U;
    const std::size_t mib = parse_nonnegative(argv[1], "MiB");
    if (mib > std::numeric_limits<std::size_t>::max() / bytes_per_mib) {
      throw std::overflow_error("requested byte count overflows size_t");
    }
    const std::size_t hold_ms =
        argc == 3 ? parse_nonnegative(argv[2], "hold duration") : 0U;

    const auto snapshot = systems_course::week02::capture_address_snapshot();
    const std::size_t byte_count = mib * bytes_per_mib;
    // No parentheses: default initialization avoids eagerly zeroing every byte.
    std::unique_ptr<std::byte[]> storage(new std::byte[byte_count]);
    const std::size_t pages = systems_course::week02::touch_one_byte_per_page(
        storage.get(), byte_count, snapshot.page_size);

    std::cout << "pid=" << snapshot.process_id << '\n'
              << "page_size=" << snapshot.page_size << '\n'
              << "global_address=" << snapshot.global_object << '\n'
              << "stack_address=" << snapshot.stack_object << '\n'
              << "heap_address=" << snapshot.heap_object << '\n'
              << "allocated_bytes=" << byte_count << '\n'
              << "touched_pages=" << pages << '\n';
    std::cout.flush();

    std::this_thread::sleep_for(std::chrono::milliseconds(hold_ms));
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "address probe failed: " << error.what() << '\n';
    return 1;
  }
}
