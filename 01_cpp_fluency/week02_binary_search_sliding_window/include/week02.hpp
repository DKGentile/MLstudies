#pragma once

#include <cstddef>
#include <string_view>
#include <vector>

namespace cpp_course::week02 {

// Returns the first index whose value is >= target, or sorted_values.size().
std::size_t first_not_less_than(const std::vector<int>& sorted_values,
                                int target);

// Searches a sorted array rotated at an unknown pivot. Values are unique.
// Returns -1 when target is absent.
std::ptrdiff_t rotated_search(const std::vector<int>& values, int target);

// Each positive pile contributes ceil(pile / speed) hours. Returns the lowest
// positive speed that finishes within hours. Throws std::invalid_argument when
// piles is empty, a pile is non-positive, or hours < piles.size().
int minimum_eating_speed(const std::vector<int>& piles, long long hours);

// For non-negative values, returns the shortest non-empty contiguous range
// with sum >= target. Returns zero if none exists or target <= 0. Throws
// std::invalid_argument if any input value is negative.
std::size_t minimum_window_length(const std::vector<int>& values,
                                  long long target);

// Returns the length of the longest contiguous byte span with no repeated byte.
std::size_t longest_unique_span(std::string_view text);

}  // namespace cpp_course::week02
