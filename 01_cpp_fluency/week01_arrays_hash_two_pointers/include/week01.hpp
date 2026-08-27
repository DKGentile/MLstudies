#pragma once

#include <cstddef>
#include <optional>
#include <string_view>
#include <utility>
#include <vector>

namespace cpp_course::week01 {

using IndexPair = std::pair<std::size_t, std::size_t>;

// Returns true exactly when some value occurs at least twice.
bool has_duplicate(const std::vector<int>& values);

// Returns any pair of distinct, ascending indices whose values sum to target.
// Returns std::nullopt when no such pair exists.
std::optional<IndexPair> two_sum_indices(const std::vector<int>& values,
                                         int target);

// Treats inputs as byte strings. Case and punctuation are significant.
bool are_anagrams(std::string_view left, std::string_view right);

// Compacts a sorted vector in place so its first returned-count elements are
// unique and sorted. Elements after that prefix have unspecified values.
std::size_t deduplicate_sorted(std::vector<int>& sorted_values);

// Chooses two vertical lines i < j and returns the maximum
// min(height[i], height[j]) * (j - i). Fewer than two lines yields zero.
long long max_container_area(const std::vector<int>& heights);

}  // namespace cpp_course::week01

