#include "week03.hpp"

#include <stdexcept>

namespace cpp_course::week03 {

bool brackets_balanced(std::string_view text) 
{
  std::string list;
  for(const char& c : text)
  {
    if(c=='(' || c=='[' || c=='{') list.push_back(c);
    else if (c==')' || c==']' || c=='}')
    {
      if(list.empty()) return false;
      switch(list.back())
      {
        case '(':
          if(c!=')') return false;
          break;
        case '{':
          if(c!='}') return false;
          break;
        case '[':
          if(c!=']') return false;
          break;
      }
      list.pop_back();
    }
    else return false;
  }
  return list.empty();
}

std::vector<std::size_t> days_until_warmer(
    const std::vector<int>& temperatures) {
  (void)temperatures;
  throw std::logic_error("TODO: implement days_until_warmer");
}

int kth_largest(const std::vector<int>& values, std::size_t k) {
  (void)values;
  (void)k;
  throw std::logic_error("TODO: implement kth_largest");
}

std::vector<Interval> merge_intervals(std::vector<Interval> intervals) {
  (void)intervals;
  throw std::logic_error("TODO: implement merge_intervals");
}

}  // namespace cpp_course::week03

