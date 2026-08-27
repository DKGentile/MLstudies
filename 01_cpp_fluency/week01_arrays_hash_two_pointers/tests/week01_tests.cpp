#include "test_support.hpp"
#include "week01.hpp"

#include <algorithm>
#include <vector>

using cpp_course::week01::are_anagrams;
using cpp_course::week01::deduplicate_sorted;
using cpp_course::week01::has_duplicate;
using cpp_course::week01::max_container_area;
using cpp_course::week01::two_sum_indices;

int main() {
  course_test::Suite suite;

  suite.run("duplicate detection handles empty, unique, and repeated data", [] {
    COURSE_CHECK(!has_duplicate({}));
    COURSE_CHECK(!has_duplicate({-3, 0, 8, 11}));
    COURSE_CHECK(has_duplicate({4, -2, 7, -2}));
  });

  suite.run("two sum returns valid distinct indices or no result", [] {
    const std::vector<int> values{8, -3, 4, 9, 1};
    const auto answer = two_sum_indices(values, 6);
    COURSE_CHECK(answer.has_value());
    COURSE_CHECK(answer->first < answer->second);
    COURSE_CHECK(answer->second < values.size());
    COURSE_CHECK(values[answer->first] + values[answer->second] == 6);
    COURSE_CHECK(!two_sum_indices(values, 100).has_value());
  });

  suite.run("anagram comparison respects multiplicity and exact bytes", [] {
    COURSE_CHECK(are_anagrams("silent", "listen"));
    COURSE_CHECK(are_anagrams("", ""));
    COURSE_CHECK(!are_anagrams("abb", "aab"));
    COURSE_CHECK(!are_anagrams("Cat", "act"));
  });

  suite.run("sorted deduplication reports and writes the unique prefix", [] {
    std::vector<int> values{-2, -2, -2, 0, 3, 3, 8};
    const std::size_t count = deduplicate_sorted(values);
    const std::vector<int> expected{-2, 0, 3, 8};
    COURSE_CHECK(count == expected.size());
    COURSE_CHECK(std::equal(expected.begin(), expected.end(), values.begin()));

    std::vector<int> empty;
    COURSE_CHECK(deduplicate_sorted(empty) == 0U);
  });

  suite.run("container area uses wide arithmetic and boundary cases", [] {
    COURSE_CHECK(max_container_area({}) == 0);
    COURSE_CHECK(max_container_area({9}) == 0);
    COURSE_CHECK(max_container_area({1, 8, 6, 2, 5, 4, 8, 3, 7}) == 49);
    COURSE_CHECK(max_container_area({1'500'000'000, 0, 1'500'000'000}) ==
                 3'000'000'000LL);
  });

  return suite.finish();
}

