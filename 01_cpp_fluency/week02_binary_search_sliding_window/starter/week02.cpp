#include "week02.hpp"

#include <stdexcept>

namespace cpp_course::week02 {

std::size_t first_not_less_than(const std::vector<int>& sorted_values, int target) 
{
  if(sorted_values.size()<1) return sorted_values.size();
  
  int left = 0, right = sorted_values.size()-1;
  while(left<right)
  {
    int mid = (right+left)/2;
    if(sorted_values[mid] >= target) right = mid;
    else left=mid+1;
  }
  return (sorted_values[left]>=target) ? left : sorted_values.size();
}



std::ptrdiff_t rotated_search(const std::vector<int>& values, int target) {
  (void)values;
  (void)target;
  throw std::logic_error("TODO: implement rotated_search");
}

int minimum_eating_speed(const std::vector<int>& piles, long long hours) {
  (void)piles;
  (void)hours;
  throw std::logic_error("TODO: implement minimum_eating_speed");
}

std::size_t minimum_window_length(const std::vector<int>& values,
                                  long long target) {
  (void)values;
  (void)target;
  throw std::logic_error("TODO: implement minimum_window_length");
}

std::size_t longest_unique_span(std::string_view text) {
  (void)text;
  throw std::logic_error("TODO: implement longest_unique_span");
}

}  // namespace cpp_course::week02

