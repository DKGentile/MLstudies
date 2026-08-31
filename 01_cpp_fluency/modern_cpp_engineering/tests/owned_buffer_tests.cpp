#include "owned_buffer.hpp"
#include "test_support.hpp"

#include <array>
#include <cstddef>
#include <limits>
#include <type_traits>
#include <utility>
#include <variant>
#include <vector>

using cpp_course::modern_cpp::ByteView;
using cpp_course::modern_cpp::ConstByteView;
using cpp_course::modern_cpp::OwnedBuffer;
using cpp_course::modern_cpp::SliceError;
using cpp_course::modern_cpp::checked_subview;

namespace {

template <typename T, typename = void>
struct can_view_rvalue : std::false_type {};

template <typename T>
struct can_view_rvalue<T,
                       std::void_t<decltype(std::declval<T&&>().view())>>
    : std::true_type {};

bool has_valid_representation(const OwnedBuffer& buffer) {
  if (buffer.size() == 0) {
    return buffer.empty() && buffer.data() == nullptr;
  }
  return !buffer.empty() && buffer.data() != nullptr;
}

}  // namespace

static_assert(!std::is_copy_constructible_v<OwnedBuffer>);
static_assert(!std::is_copy_assignable_v<OwnedBuffer>);
static_assert(std::is_nothrow_default_constructible_v<OwnedBuffer>);
static_assert(std::is_nothrow_destructible_v<OwnedBuffer>);
static_assert(std::is_nothrow_move_constructible_v<OwnedBuffer>);
static_assert(std::is_nothrow_move_assignable_v<OwnedBuffer>);
static_assert(!can_view_rvalue<OwnedBuffer>::value);
static_assert(std::is_same_v<decltype(std::declval<OwnedBuffer&>().data()),
                             std::byte*>);
static_assert(
    std::is_same_v<decltype(std::declval<const OwnedBuffer&>().data()),
                   const std::byte*>);
static_assert(std::is_same_v<decltype(std::declval<OwnedBuffer&>().view()),
                             ByteView>);
static_assert(
    std::is_same_v<decltype(std::declval<const OwnedBuffer&>().view()),
                   ConstByteView>);

int main() {
  course_test::Suite suite;

  suite.run("default and zero-sized buffers have one explicit empty state", [] {
    const OwnedBuffer default_buffer;
    COURSE_CHECK(has_valid_representation(default_buffer));
    COURSE_CHECK(default_buffer.empty());

    const OwnedBuffer zero_buffer(0);
    COURSE_CHECK(has_valid_representation(zero_buffer));
    COURSE_CHECK(zero_buffer.empty());
  });

  suite.run("mutable and const access refer to the owned bytes", [] {
    OwnedBuffer buffer(4);
    COURSE_CHECK(has_valid_representation(buffer));
    COURSE_CHECK(buffer.size() == 4U);

    buffer.data()[0] = std::byte{0x11};
    buffer.data()[3] = std::byte{0xA5};
    const OwnedBuffer& read_only = buffer;
    COURSE_CHECK(read_only.data()[0] == std::byte{0x11});
    COURSE_CHECK(read_only.data()[3] == std::byte{0xA5});

    ByteView writable = buffer.view();
    const ConstByteView readable = read_only.view();
    COURSE_CHECK(writable.data == buffer.data());
    COURSE_CHECK(writable.size == buffer.size());
    COURSE_CHECK(readable.data == buffer.data());
    COURSE_CHECK(readable.size == buffer.size());
    writable.data[1] = std::byte{0x7F};
    COURSE_CHECK(readable.data[1] == std::byte{0x7F});
  });

  suite.run("move construction transfers identity and empties the source", [] {
    OwnedBuffer source(3);
    source.data()[0] = std::byte{0x2A};
    std::byte* const original_data = source.data();

    OwnedBuffer destination(std::move(source));
    COURSE_CHECK(has_valid_representation(source));
    COURSE_CHECK(source.empty());
    COURSE_CHECK(has_valid_representation(destination));
    COURSE_CHECK(destination.size() == 3U);
    COURSE_CHECK(destination.data() == original_data);
    COURSE_CHECK(destination.data()[0] == std::byte{0x2A});
  });

  suite.run("move assignment replaces an existing owned resource", [] {
    OwnedBuffer source(5);
    source.data()[4] = std::byte{0x55};
    std::byte* const source_data = source.data();
    OwnedBuffer destination(2);
    destination.data()[0] = std::byte{0xEE};

    destination = std::move(source);
    COURSE_CHECK(has_valid_representation(source));
    COURSE_CHECK(source.empty());
    COURSE_CHECK(has_valid_representation(destination));
    COURSE_CHECK(destination.size() == 5U);
    COURSE_CHECK(destination.data() == source_data);
    COURSE_CHECK(destination.data()[4] == std::byte{0x55});
  });

  suite.run("self-move and container relocation preserve a valid owner", [] {
    OwnedBuffer buffer(2);
    buffer.data()[1] = std::byte{0x31};
    buffer = std::move(buffer);
    COURSE_CHECK(has_valid_representation(buffer));

    OwnedBuffer first(1);
    first.data()[0] = std::byte{0x6C};
    std::byte* const first_data = first.data();
    std::vector<OwnedBuffer> buffers;
    buffers.push_back(std::move(first));
    buffers.emplace_back(8);
    COURSE_CHECK(first.empty());
    COURSE_CHECK(buffers[0].data() == first_data);
    COURSE_CHECK(buffers[0].data()[0] == std::byte{0x6C});
    COURSE_CHECK(has_valid_representation(buffers[1]));
  });

  suite.run("checked subviews model success and precise failure alternatives", [] {
    const std::array<std::byte, 4> bytes{
        std::byte{0x10}, std::byte{0x20}, std::byte{0x30}, std::byte{0x40}};
    const ConstByteView whole{bytes.data(), bytes.size()};

    const auto middle = checked_subview(whole, 1, 2);
    COURSE_CHECK(std::holds_alternative<ConstByteView>(middle));
    const auto middle_view = std::get<ConstByteView>(middle);
    COURSE_CHECK(middle_view.data == bytes.data() + 1);
    COURSE_CHECK(middle_view.size == 2U);
    COURSE_CHECK(middle_view.data[0] == std::byte{0x20});

    const auto end = checked_subview(whole, bytes.size(), 0);
    COURSE_CHECK(std::holds_alternative<ConstByteView>(end));
    COURSE_CHECK(std::get<ConstByteView>(end).size == 0U);

    COURSE_CHECK(std::get<SliceError>(checked_subview(whole, 5, 0)) ==
                 SliceError::offset_out_of_range);
    COURSE_CHECK(std::get<SliceError>(checked_subview(whole, 3, 2)) ==
                 SliceError::length_out_of_range);
    COURSE_CHECK(
        std::get<SliceError>(checked_subview(
            whole, std::numeric_limits<std::size_t>::max(), 2)) ==
        SliceError::offset_out_of_range);

    const auto empty = checked_subview(ConstByteView{}, 0, 0);
    COURSE_CHECK(std::holds_alternative<ConstByteView>(empty));
    COURSE_CHECK(std::get<ConstByteView>(empty).data == nullptr);
    COURSE_CHECK(std::get<ConstByteView>(empty).size == 0U);
  });

  return suite.finish();
}
