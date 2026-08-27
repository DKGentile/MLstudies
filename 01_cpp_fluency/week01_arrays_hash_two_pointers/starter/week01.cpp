#include "week01.hpp"

#include <stdexcept>
#include<unordered_map>

namespace cpp_course::week01 {

bool has_duplicate(const std::vector<int>& values) {
  if (values.size()<= 1) {return false;}
  for (int i = 0; i < values.size(); i++)
  {
    for (int j = i+1; j<values.size(); j++ )
    {
      if (values[i]==values[j]) {return true;}
    }
  }  
  return false;
}

std::optional<IndexPair> two_sum_indices(const std::vector<int>& values, int target) {
  if (values.size()<=1){return std::nullopt;}
  for (int i = 0; i < values.size(); i++)
  {
    for (int j = i+1; j<values.size(); j++)
    {
      if (values[i]+values[j]==target) { return IndexPair{i,j}; }
    }
  }
  return std::nullopt;
}

bool are_anagrams(std::string_view left, std::string_view right) 
{
  if (left.size()!=right.size()) {return false;}

  int count[256]{};
  for (int i = 0; i < left.size(); i++)
  {
    count[static_cast<unsigned char>(left[i])] += 1;
    count[static_cast<unsigned char>(right[i])] -= 1;
  }
  for (int i = 0; i < 256; i++)
  {
    if (count[i]!=0) {return false;}
  }
  return true;
}

std::size_t deduplicate_sorted(std::vector<int>& sorted_values) {
  if (sorted_values.size()<=1){return sorted_values.size();}
  int c = 1;
  std::optional<int> x = std::nullopt;
  for (int i = 1; i < sorted_values.size(); i++)
  {
    if (sorted_values[i] == sorted_values[i-1] && !x.has_value())
    {
      x = i;
    }
    else if (x && sorted_values[i] != sorted_values[i-1])
    {
      sorted_values[x.value()] = sorted_values[i];
      x = x.value() + 1;
      c++;
    }
    else if (!x.has_value() && sorted_values[i] != sorted_values[i-1]){c++;}
  }
  return c;
}

long long max_container_area(const std::vector<int>& heights) {
  (void)heights;
  throw std::logic_error("TODO: implement max_container_area");
}

}  // namespace cpp_course::week01

