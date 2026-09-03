#include "week02.hpp"

#include <stdexcept>

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
  if(piles.size()<1 || piles.size()>hours) throw std::invalid_argument("NO BANANAS!");
  if(piles.size()==1) return static_cast<long long>(piles[0])/hours;

  int speed = *std::max(piles.begin(),piles.end()), temp_hours = 0;

  while(temp_hours<hours)
  {
    for(int i = 0; i < piles.size(); i++)
    {
      temp_hours+= (piles[i]+speed-1)/speed;
      if(temp_hours>hours) break;
    }
    if(temp_hours>hours;)
    {
      
    }
  }

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

