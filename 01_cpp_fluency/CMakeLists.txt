cmake_minimum_required(VERSION 3.21)
project(cpp_fluency_phase0 LANGUAGES CXX)

include(CTest)

function(course_target target)
  target_compile_features(${target} PRIVATE cxx_std_17)
  if(MSVC)
    target_compile_options(${target} PRIVATE /W4 /permissive-)
  else()
    target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic)
  endif()
endfunction()

function(add_course_week week slug)
  set(lib "cpp_${week}_lib")
  set(test "cpp_${week}_tests")

  add_library(${lib} "${slug}/starter/${week}.cpp")
  target_include_directories(${lib} PUBLIC "${slug}/include")
  course_target(${lib})

  add_executable(${test} "${slug}/tests/${week}_tests.cpp")
  target_include_directories(${test} PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/common")
  target_link_libraries(${test} PRIVATE ${lib})
  course_target(${test})

  add_test(NAME ${test} COMMAND ${test})
endfunction()

add_course_week(week01 week01_arrays_hash_two_pointers)
add_course_week(week02 week02_binary_search_sliding_window)
add_course_week(week03 week03_stacks_heaps_intervals)
add_course_week(week04 week04_trees_graphs)
