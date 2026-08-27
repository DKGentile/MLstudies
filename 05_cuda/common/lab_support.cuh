#pragma once

#include <cuda_runtime.h>

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

#define CUDA_CHECK(expression)                                                   \
  do {                                                                           \
    const cudaError_t cuda_status_ = (expression);                               \
    if (cuda_status_ != cudaSuccess) {                                           \
      throw std::runtime_error(std::string("CUDA error at ") + __FILE__ + ":" + \
                               std::to_string(__LINE__) + ": " +                \
                               cudaGetErrorString(cuda_status_));                 \
    }                                                                            \
  } while (false)

namespace lab {

template <typename T>
class DeviceBuffer {
 public:
  explicit DeviceBuffer(std::size_t count) : count_(count) {
    if (count_ != 0) {
      CUDA_CHECK(cudaMalloc(reinterpret_cast<void**>(&data_), bytes()));
    }
  }

  ~DeviceBuffer() {
    if (data_ != nullptr) {
      cudaFree(data_);
    }
  }

  DeviceBuffer(const DeviceBuffer&) = delete;
  DeviceBuffer& operator=(const DeviceBuffer&) = delete;

  DeviceBuffer(DeviceBuffer&& other) noexcept
      : data_(std::exchange(other.data_, nullptr)),
        count_(std::exchange(other.count_, 0)) {}

  T* data() { return data_; }
  const T* data() const { return data_; }
  std::size_t size() const { return count_; }
  std::size_t bytes() const { return count_ * sizeof(T); }

  void copy_from(const std::vector<T>& host) {
    if (host.size() != count_) {
      throw std::invalid_argument("host/device size mismatch");
    }
    CUDA_CHECK(cudaMemcpy(data_, host.data(), bytes(), cudaMemcpyHostToDevice));
  }

  void copy_to(std::vector<T>& host) const {
    if (host.size() != count_) {
      throw std::invalid_argument("host/device size mismatch");
    }
    CUDA_CHECK(cudaMemcpy(host.data(), data_, bytes(), cudaMemcpyDeviceToHost));
  }

 private:
  T* data_ = nullptr;
  std::size_t count_ = 0;
};

class EventPair {
 public:
  EventPair() {
    CUDA_CHECK(cudaEventCreate(&start_));
    CUDA_CHECK(cudaEventCreate(&stop_));
  }

  ~EventPair() {
    cudaEventDestroy(start_);
    cudaEventDestroy(stop_);
  }

  EventPair(const EventPair&) = delete;
  EventPair& operator=(const EventPair&) = delete;

  cudaEvent_t start() const { return start_; }
  cudaEvent_t stop() const { return stop_; }

 private:
  cudaEvent_t start_{};
  cudaEvent_t stop_{};
};

template <typename Launch>
double median_kernel_ms(Launch&& launch, int warmups = 5, int iterations = 50,
                        int samples = 7) {
  if (warmups < 0 || iterations <= 0 || samples <= 0) {
    throw std::invalid_argument("invalid benchmark repetition count");
  }

  for (int i = 0; i < warmups; ++i) {
    launch();
  }
  CUDA_CHECK(cudaGetLastError());
  CUDA_CHECK(cudaDeviceSynchronize());

  EventPair events;
  std::vector<float> measurements;
  measurements.reserve(static_cast<std::size_t>(samples));
  for (int sample = 0; sample < samples; ++sample) {
    CUDA_CHECK(cudaEventRecord(events.start()));
    for (int i = 0; i < iterations; ++i) {
      launch();
    }
    CUDA_CHECK(cudaEventRecord(events.stop()));
    CUDA_CHECK(cudaEventSynchronize(events.stop()));
    CUDA_CHECK(cudaGetLastError());
    float batch_ms = 0.0F;
    CUDA_CHECK(cudaEventElapsedTime(&batch_ms, events.start(), events.stop()));
    measurements.push_back(batch_ms / static_cast<float>(iterations));
  }

  std::sort(measurements.begin(), measurements.end());
  return static_cast<double>(measurements[measurements.size() / 2]);
}

inline cudaDeviceProp print_device_summary() {
  int device = 0;
  CUDA_CHECK(cudaGetDevice(&device));
  cudaDeviceProp properties{};
  CUDA_CHECK(cudaGetDeviceProperties(&properties, device));
  int runtime_version = 0;
  CUDA_CHECK(cudaRuntimeGetVersion(&runtime_version));
  std::cout << "device=" << properties.name << " cc=" << properties.major << '.'
            << properties.minor << " runtime=" << runtime_version << '\n';
  return properties;
}

inline std::size_t parse_size_or(const char* text, std::size_t fallback) {
  if (text == nullptr) {
    return fallback;
  }
  const std::string value(text);
  std::size_t consumed = 0;
  const unsigned long long parsed = std::stoull(value, &consumed);
  if (consumed != value.size() || parsed == 0) {
    throw std::invalid_argument("size must be a positive integer");
  }
  return static_cast<std::size_t>(parsed);
}

template <typename T>
bool check_close(const std::vector<T>& expected, const std::vector<T>& actual,
                 double absolute_tolerance, double relative_tolerance) {
  if (expected.size() != actual.size()) {
    std::cerr << "FAIL: result size mismatch\n";
    return false;
  }

  std::size_t mismatch_count = 0;
  std::size_t worst_index = 0;
  double worst_error = 0.0;
  for (std::size_t i = 0; i < expected.size(); ++i) {
    const double reference = static_cast<double>(expected[i]);
    const double candidate = static_cast<double>(actual[i]);
    const double error = std::abs(reference - candidate);
    const double allowed = absolute_tolerance + relative_tolerance * std::abs(reference);
    if (!std::isfinite(candidate) || error > allowed) {
      ++mismatch_count;
      if (error > worst_error || !std::isfinite(candidate)) {
        worst_error = error;
        worst_index = i;
      }
    }
  }

  if (mismatch_count != 0) {
    std::cerr << "FAIL: " << mismatch_count << " mismatches; index " << worst_index
              << " expected=" << expected[worst_index]
              << " actual=" << actual[worst_index]
              << " abs_error=" << worst_error << '\n';
    return false;
  }
  std::cout << "PASS: " << expected.size() << " values match the CPU reference\n";
  return true;
}

}  // namespace lab
