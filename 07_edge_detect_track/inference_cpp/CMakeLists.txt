cmake_minimum_required(VERSION 3.20)
project(edge_detect_track_infer LANGUAGES CXX)

add_executable(edge_infer main.cpp)
target_compile_features(edge_infer PRIVATE cxx_std_17)

if(MSVC)
  target_compile_options(edge_infer PRIVATE /W4 /permissive-)
else()
  target_compile_options(edge_infer PRIVATE -Wall -Wextra -Wpedantic)
endif()

