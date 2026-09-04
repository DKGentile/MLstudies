#include "week02.hpp"

#include <stdexcept>
#include <algorithm>

namespace cpp_course::week02 {

std::size_t first_not_less_than(const std::vector<int>& sorted_values, int target) 
{
  if(sorted_values.size()<1) return sorted_values.size();
  
  size_t left = 0, right = sorted_values.size()-1;
  while(left<right)
  {
    size_t mid = (right+left)/2;
    if(sorted_values[mid] >= target) right = mid;
    else left=mid+1;
  }
  return (sorted_values[left]>=target) ? left : sorted_values.size();
}



std::ptrdiff_t rotated_search(const std::vector<int>& values, int target) 
{
   if(values.size()<1) return -1;
   if(values.size()==1) return (values[0]==target) ? 0 : -1;

   std::ptrdiff_t left=0, right = values.size()-1;

   while(left<=right)
   {
      std::ptrdiff_t mid = (left+right)/2;
      if(values[mid]==target) return mid;

      if(values[left]<=values[mid]) //L->M is sorted 
      { 
        if(values[left]<=target && values[mid]>target) right = mid - 1;
        else left=mid+1;
      }
      else //M->R is sorted
      {
        if(values[mid]<target && values[right] >= target) left = mid+1;
        else right = mid-1;
      }
   }
   return -1;
}


int minimum_eating_speed(const std::vector<int>& piles, long long hours) {
  if( 1 > piles.size() || hours < static_cast<long long>(piles.size()) )  
  throw std::invalid_argument("NO BANANA TIME!");

  auto [min_it, max_it] = std::minmax_element(piles.begin(), piles.end());

  int minimum = *min_it;
  int maximum = *max_it;

  if(minimum < 1 || maximum < 1) throw std::invalid_argument("NO BANANS!");

  while(minimum<maximum)
  {
    int temp_speed = minimum + (maximum-minimum)/2;
    long long temp_hours = 0;
    for(int pile : piles)
    {
      temp_hours += (pile + temp_speed - 1) / temp_speed;
      if(temp_hours>hours) break;
    }
    if(temp_hours<=hours) maximum = temp_speed;
    else minimum = temp_speed+1;
  }
  return minimum;
}

std::size_t minimum_window_length(const std::vector<int>& values, long long target) 
{
  for(const int& x : values) if (x<0) throw std::invalid_argument("Negative value in 'values'.");
  //comment out previous line for efficiency. 
  if(values.empty() || target<=0) return 0;
  

  std::size_t window = values.size(), begin = 0;
  long long temp_sum = 0;
  
  for(size_t i = 0; i < values.size(); i++)
  {
    //if(values[i]<0) throw std::invalid_argument("Negative value in 'values'.");
    //uncomment if initial negative check is
    temp_sum+=values[i];
    if(temp_sum>=target)
    {
      for(size_t j = begin; j <= i; j++)
      {
        
        if(temp_sum-values[j]<target)
        {
          begin = j;
          break;
        }
        temp_sum-=values[j];
      }
      std::size_t temp_window = i-begin+1;
      if(window>temp_window) window = temp_window;
      if(window == 1) return window;
    }
  }
  return (temp_sum>=target) ? window : 0;
}

std::size_t longest_unique_span(std::string_view text) {
  (void)text;
  throw std::logic_error("TODO: implement longest_unique_span");
}

}  // namespace cpp_course::week02

