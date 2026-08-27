#include "test_support.hpp"
#include "week02.hpp"

#include <stdexcept>
#include <vector>

using cpp_course::week02::first_not_less_than;
using cpp_course::week02::longest_unique_span;
using cpp_course::week02::minimum_eating_speed;
using cpp_course::week02::minimum_window_length;
using cpp_course::week02::rotated_search;

namespace {

template <typename Function>
bool throws_invalid_argument(Function&& function) {
  try {
    function();
  } catch (const std::invalid_argument&) {
    return true;
  }
  return false;
}

}  // namespace

int main() {
  course_test::Suite suite;

  suite.run("lower-bound search returns a boundary or end sentinel", [] {
    const std::vector<int> values{-5, -1, 2, 2, 9};
    COURSE_CHECK(first_not_less_than(values, -10) == 0U);
    COURSE_CHECK(first_not_less_than(values, 2) == 2U);
    COURSE_CHECK(first_not_less_than(values, 3) == 4U);
    COURSE_CHECK(first_not_less_than(values, 10) == values.size());
    COURSE_CHECK(first_not_less_than({}, 0) == 0U);
  });

  suite.run("rotated search finds either sorted segment", [] {
    const std::vector<int> values{13, 18, 2, 4, 7, 9};
    COURSE_CHECK(rotated_search(values, 18) == 1);
    COURSE_CHECK(rotated_search(values, 7) == 4);
    COURSE_CHECK(rotated_search(values, 6) == -1);
    COURSE_CHECK(rotated_search({5}, 5) == 0);
    COURSE_CHECK(rotated_search({}, 5) == -1);
  });

  suite.run("minimum feasible speed honors the deadline", [] {
    COURSE_CHECK(minimum_eating_speed({3, 6, 7, 11}, 8) == 4);
    COURSE_CHECK(minimum_eating_speed({30, 11, 23, 4, 20}, 5) == 30);
    COURSE_CHECK(minimum_eating_speed({1, 1, 1}, 100) == 1);
    COURSE_CHECK(throws_invalid_argument(
        [] { (void)minimum_eating_speed({}, 1); }));
    COURSE_CHECK(throws_invalid_argument(
        [] { (void)minimum_eating_speed({3, 0}, 2); }));
    COURSE_CHECK(throws_invalid_argument(
        [] { (void)minimum_eating_speed({3, 4}, 1); }));
  });

  suite.run("minimum positive-sum window is minimal and contiguous", [] {
    COURSE_CHECK(minimum_window_length({2, 3, 1, 2, 4, 3}, 7) == 2U);
    COURSE_CHECK(minimum_window_length({1, 1, 1}, 5) == 0U);
    COURSE_CHECK(minimum_window_length({9, 1, 1}, 9) == 1U);
    COURSE_CHECK(minimum_window_length({}, 1) == 0U);
    COURSE_CHECK(minimum_window_length({1, 2}, 0) == 0U);
    COURSE_CHECK(throws_invalid_argument(
        [] { (void)minimum_window_length({2, -1, 3}, 3); }));
  });

  suite.run("longest unique span handles repeats at both boundaries", [] {
    COURSE_CHECK(longest_unique_span("") == 0U);
    COURSE_CHECK(longest_unique_span("abcabcbb") == 3U);
    COURSE_CHECK(longest_unique_span("bbbbb") == 1U);
    COURSE_CHECK(longest_unique_span("abba") == 2U);
    COURSE_CHECK(longest_unique_span("dvdf") == 3U);
  });

  return suite.finish();
}
