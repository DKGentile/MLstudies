cmake_minimum_required(VERSION 3.24)

project(mlstudies_gpu_optimization LANGUAGES NONE)

option(MLSTUDIES_ENABLE_CUDA "Build the GPU optimization exercises" ON)

if(NOT MLSTUDIES_ENABLE_CUDA)
  message(STATUS "MLSTUDIES_ENABLE_CUDA=OFF: GPU optimization labs are intentionally skipped")
  add_custom_target(gpu_optimization_skipped ALL
    COMMAND ${CMAKE_COMMAND} -E echo "GPU optimization labs skipped; run tests/validate_course.py for CPU-only validation"
    VERBATIM)
  return()
endif()

include(CheckLanguage)
check_language(CUDA)

if(NOT CMAKE_CUDA_COMPILER)
  message(STATUS "No CUDA compiler found: GPU optimization labs will not be built")
  add_custom_target(gpu_optimization_skipped ALL
    COMMAND ${CMAKE_COMMAND} -E echo "CUDA compiler unavailable; GPU optimization targets were skipped"
    VERBATIM)
  return()
endif()

if(NOT DEFINED CMAKE_CUDA_ARCHITECTURES)
  set(CMAKE_CUDA_ARCHITECTURES native CACHE STRING "CUDA architectures")
endif()

enable_language(CXX)
enable_language(CUDA)
find_package(CUDAToolkit REQUIRED)

if(NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

set(_targets_pascal FALSE)
set(_targets_blackwell_120 FALSE)
foreach(_architecture IN LISTS CMAKE_CUDA_ARCHITECTURES)
  if(_architecture MATCHES "^61(-real|-virtual)?$")
    set(_targets_pascal TRUE)
  elseif(_architecture MATCHES "^120(-real|-virtual)?$")
    set(_targets_blackwell_120 TRUE)
  endif()
endforeach()

if(_targets_pascal AND CUDAToolkit_VERSION VERSION_GREATER_EQUAL 13.0)
  message(FATAL_ERROR
    "CUDA ${CUDAToolkit_VERSION} cannot compile GTX 1080/Pascal sm_61. "
    "Use a CUDA 12.x toolkit for -DCMAKE_CUDA_ARCHITECTURES=61.")
endif()
if(_targets_blackwell_120 AND CUDAToolkit_VERSION VERSION_LESS 12.8)
  message(FATAL_ERROR
    "CUDA ${CUDAToolkit_VERSION} predates sm_120 support. "
    "Use CUDA 12.8 or newer for -DCMAKE_CUDA_ARCHITECTURES=120.")
endif()
if(CUDAToolkit_VERSION VERSION_GREATER_EQUAL 13.0 AND
   "${CMAKE_CUDA_ARCHITECTURES}" STREQUAL "native")
  message(STATUS
    "CUDA ${CUDAToolkit_VERSION} with native architecture cannot target a GTX 1080; "
    "use CUDA 12.x on the Pascal machine")
endif()
message(STATUS
  "CUDA toolkit ${CUDAToolkit_VERSION}; architectures=${CMAKE_CUDA_ARCHITECTURES}")

function(add_gpu_optimization_lab target source)
  add_executable(${target} ${source})
  target_include_directories(${target} PRIVATE ${PROJECT_SOURCE_DIR}/common)
  target_link_libraries(${target} PRIVATE CUDA::cudart)
  target_compile_features(${target} PRIVATE cxx_std_17 cuda_std_17)
  target_compile_options(${target} PRIVATE $<$<COMPILE_LANGUAGE:CUDA>:-lineinfo>)
  set_target_properties(${target} PROPERTIES
    CUDA_SEPARABLE_COMPILATION ON
    CUDA_ARCHITECTURES "${CMAKE_CUDA_ARCHITECTURES}")
endfunction()

add_subdirectory(01_coalescing)
add_subdirectory(02_tiled_blur)
add_subdirectory(03_privatized_histogram)
