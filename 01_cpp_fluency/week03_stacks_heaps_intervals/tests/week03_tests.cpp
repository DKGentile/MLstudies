#include "test_support.hpp"
#include "week03.hpp"

#include <stdexcept>
#include <vector>

using cpp_course::week03::Interval;
using cpp_course::week03::brackets_balanced;
using cpp_course::week03::days_until_warmer;
using cpp_course::week03::kth_largest;
using cpp_course::week03::merge_intervals;

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

  suite.run("bracket stack accepts exact nesting and rejects malformed input", [] {
    COURSE_CHECK(brackets_balanced(""));
    COURSE_CHECK(brackets_balanced("{[()()]()}"));
    COURSE_CHECK(!brackets_balanced("([)]"));
    COURSE_CHECK(!brackets_balanced("(()"));
    COURSE_CHECK(!brackets_balanced("(x)"));
  });

  suite.run("monotonic stack reports the next strictly warmer position", [] {
    const std::vector<std::size_t> expected{1, 1, 4, 2, 1, 1, 0, 0};
    COURSE_CHECK(days_until_warmer({73, 74, 75, 71, 69, 72, 76, 73}) ==
                 expected);
    COURSE_CHECK(days_until_warmer({30, 30, 30}) ==
                 std::vector<std::size_t>({0, 0, 0}));
    COURSE_CHECK(days_until_warmer({}) == std::vector<std::size_t>{});
  });

  suite.run("bounded heap selects k-th largest while counting duplicates", [] {
    COURSE_CHECK(kth_largest({3, 2, 1, 5, 6, 4}, 2) == 5);
    COURSE_CHECK(kth_largest({3, 2, 3, 1, 2, 4, 5, 5, 6}, 4) == 4);
    COURSE_CHECK(kth_largest({-7}, 1) == -7);
    COURSE_CHECK(throws_invalid_argument([] { (void)kth_largest({1}, 0); }));
    COURSE_CHECK(throws_invalid_argument([] { (void)kth_largest({1}, 2); }));
  });

  suite.run("closed intervals merge overlap, touching, and containment", [] {
    const std::vector<Interval> input{{8, 10}, {1, 3}, {2, 6}, {15, 18}};
    const std::vector<Interval> expected{{1, 6}, {8, 10}, {15, 18}};
    COURSE_CHECK(merge_intervals(input) == expected);

    COURSE_CHECK(merge_intervals({{1, 4}, {4, 5}}) ==
                 std::vector<Interval>({{1, 5}}));
    COURSE_CHECK(merge_intervals({{1, 10}, {3, 4}}) ==
                 std::vector<Interval>({{1, 10}}));
    COURSE_CHECK(merge_intervals({}).empty());
    COURSE_CHECK(throws_invalid_argument(
        [] { (void)merge_intervals({{5, 2}}); }));
  });

  return suite.finish();
}
