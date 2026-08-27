#pragma once

#include <cstddef>
#include <string_view>
#include <vector>

namespace cpp_course::week03 {

struct Interval {
  int start;
  int end;
};

inline bool operator==(const Interval& left, const Interval& right) {
  return left.start == right.start && left.end == right.end;
}

// Accepts only (), [], and {} characters. Returns false for an unexpected byte,
// a mismatched closer, or an unclosed opener. Empty input is balanced.
bool brackets_balanced(std::string_view text);

// For each day, returns how many later positions must pass before a strictly
// greater temperature appears, or zero when it never does.
std::vector<std::size_t> days_until_warmer(
    const std::vector<int>& temperatures);

// Returns the k-th largest value counting duplicates. Throws
// std::invalid_argument when k == 0 or k > values.size().
int kth_largest(const std::vector<int>& values, std::size_t k);

// Merges overlapping closed intervals. Touching endpoints overlap. Output is
// sorted by start. Throws std::invalid_argument if any start > end.
std::vector<Interval> merge_intervals(std::vector<Interval> intervals);

}  // namespace cpp_course::week03

