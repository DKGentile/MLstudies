#include "week01.hpp"

#include <stdexcept>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>

namespace cpp_course::week01 {

bool has_duplicate(const std::vector<int>& values) 
{
  if (values.size()<= 1) 
  { return false; }

  std::unordered_set<int> value_index;
  for (int i = 0; i < values.size(); i++)
  {
    if(value_index.find(values[i])==value_index.end())
    { value_index.insert(values[i]); }

    else 
    { return true; }
  }

  return false;
}

std::optional<IndexPair> two_sum_indices(const std::vector<int>& values, int target) 
{
  if (values.size()<=1)
  { return std::nullopt; }
  
  std::unordered_map<int,int> value_index; //value, index
  for (int i = 0; i < values.size(); i++)
  {
    if (value_index.find(target-values[i])!= value_index.end())
    { return IndexPair{value_index[target-values[i]],i}; }

    else
    { value_index[values[i]]=i; }
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
    if (count[i]!=0) 
    { return false; }
  }

  return true;
}

std::size_t deduplicate_sorted(std::vector<int>& sorted_values) {
  if (sorted_values.size()<=1)
  { return sorted_values.size(); }

  int size_counter = 1;
  std::optional<int> duped_index = std::nullopt;
  for (int i = 1; i < sorted_values.size(); i++)
  {
    if (sorted_values[i] == sorted_values[i-1] && !duped_index.has_value())
    { duped_index = i; }

    else if (duped_index && sorted_values[i] != sorted_values[i-1])
    {
      sorted_values[duped_index.value()] = sorted_values[i];
      duped_index = duped_index.value() + 1;
      size_counter++;
    }

    else if (!duped_index.has_value() && sorted_values[i] != sorted_values[i-1])
    { size_counter++; }
  }

  return size_counter;
}

long long get_area(const int &side1,const int &side2, const int &distance)
{
  return static_cast<long long>(std::min(side1,side2)) * static_cast<long long>(distance);
}

long long max_container_area(const std::vector<int>& heights) 
{
  if (heights.size() < 2){return 0;}
  int left = 0, right = heights.size()-1;
  long long area = 0;
  while (left<right)
  {
    long long new_area = get_area(heights[left],heights[right], right-left);
    if (new_area > area) 
    { area = new_area; }

    if(heights[left]>heights[right]) { right--; }
    else { left++; }
  }
  return area;
}

}  // namespace cpp_course::week01

