#include "address_space.hpp"
#include "test_support.hpp"

#include <cstddef>
#include <stdexcept>
#include <vector>

using systems_course::week02::capture_address_snapshot;
using systems_course::week02::touch_one_byte_per_page;

int main() {
  course_test::Suite suite;

  suite.run("snapshot reports plausible nonzero process and object data", [] {
    const auto snapshot = capture_address_snapshot();
    COURSE_CHECK(snapshot.process_id > 0U);
    COURSE_CHECK(snapshot.page_size >= 512U);
    COURSE_CHECK(snapshot.page_size <= 1024U * 1024U);
    COURSE_CHECK(snapshot.global_object != 0U);
    COURSE_CHECK(snapshot.stack_object != 0U);
    COURSE_CHECK(snapshot.heap_object != 0U);
    COURSE_CHECK(snapshot.global_object != snapshot.stack_object);
    COURSE_CHECK(snapshot.stack_object != snapshot.heap_object);
  });

  suite.run("page touch writes exactly one leading byte per page", [] {
    constexpr std::size_t page_size = 16;
    std::vector<std::byte> storage(35, std::byte{0});
    const std::size_t count =
        touch_one_byte_per_page(storage.data(), storage.size(), page_size);
    COURSE_CHECK(count == 3U);
    COURSE_CHECK(storage[0] == std::byte{0xA5});
    COURSE_CHECK(storage[16] == std::byte{0xA5});
    COURSE_CHECK(storage[32] == std::byte{0xA5});
    COURSE_CHECK(storage[1] == std::byte{0});
    COURSE_CHECK(storage[34] == std::byte{0});

    COURSE_CHECK(touch_one_byte_per_page(nullptr, 0, page_size) == 0U);
  });

  suite.run("zero page size is rejected deliberately", [] {
    std::vector<std::byte> storage(1);
    bool saw_expected_exception = false;
    try {
      (void)touch_one_byte_per_page(storage.data(), storage.size(), 0);
    } catch (const std::invalid_argument&) {
      saw_expected_exception = true;
    }
    COURSE_CHECK(saw_expected_exception);

    bool rejected_null_range = false;
    try {
      (void)touch_one_byte_per_page(nullptr, 1, 16);
    } catch (const std::invalid_argument&) {
      rejected_null_range = true;
    }
    COURSE_CHECK(rejected_null_range);
  });

  return suite.finish();
}
