#include "benchmark.cuh"

#include <algorithm>
#include <array>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

constexpr int kBinCount = 256;

__global__ void global_atomic_histogram_kernel(const std::uint8_t* input,
                                               std::size_t count,
                                               unsigned int* bins) {
  const std::size_t start =
      static_cast<std::size_t>(blockIdx.x) * blockDim.x + threadIdx.x;
  const std::size_t stride =
      static_cast<std::size_t>(blockDim.x) * gridDim.x;
  for (std::size_t i = start; i < count; i += stride) {
    atomicAdd(&bins[input[i]], 1U);
  }
}

__global__ void shared_histogram_kernel(const std::uint8_t* input,
                                        std::size_t count,
                                        unsigned int* bins) {
  extern __shared__ unsigned int local_bins[];

  // TODO(learner): Cooperatively clear local_bins, fill it with a grid-stride
  // loop and shared-memory atomics, then cooperatively merge it into global
  // bins. Put barriers exactly where cross-thread data dependencies require.
  (void)input;
  (void)count;
  (void)bins;
  (void)local_bins;
}

bool check_histogram(const std::array<unsigned int, kBinCount>& expected,
                     const std::vector<unsigned int>& actual,
                     const char* label) {
  std::size_t mismatches = 0;
  for (int bin = 0; bin < kBinCount; ++bin) {
    if (expected[bin] != actual[bin]) {
      if (mismatches < 5) {
        std::cerr << label << " bin=" << bin << " expected=" << expected[bin]
                  << " actual=" << actual[bin] << '\n';
      }
      ++mismatches;
    }
  }
  if (mismatches != 0) {
    std::cerr << "FAIL " << label << ": mismatched_bins=" << mismatches << '\n';
    return false;
  }
  std::cout << "PASS " << label << ": all bins match\n";
  return true;
}

std::array<unsigned int, kBinCount> fill_distribution(
    std::vector<std::uint8_t>& input, unsigned int active_bins) {
  std::array<unsigned int, kBinCount> expected{};
  for (std::size_t i = 0; i < input.size(); ++i) {
    input[i] = static_cast<std::uint8_t>((i * 37U) % active_bins);
    ++expected[input[i]];
  }
  return expected;
}

int main(int argc, char** argv) {
  try {
    const std::size_t count = bench::parse_size_or(
        argc > 1 ? argv[1] : nullptr, (1U << 22U) + 19U);
    const cudaDeviceProp properties = bench::print_device_summary();

    std::vector<std::uint8_t> input(count);
    const auto full_range_expected = fill_distribution(input, kBinCount);

    bench::DeviceBuffer<std::uint8_t> d_input(count);
    bench::DeviceBuffer<unsigned int> d_global(kBinCount), d_shared(kBinCount);
    d_input.copy_from(input);

    constexpr int threads = 256;
    const int blocks = std::min(256, properties.multiProcessorCount * 8);
    constexpr std::size_t shared_bytes = kBinCount * sizeof(unsigned int);
    const auto launch_global = [&] {
      global_atomic_histogram_kernel<<<blocks, threads>>>(
          d_input.data(), count, d_global.data());
    };
    const auto launch_shared = [&] {
      shared_histogram_kernel<<<blocks, threads, shared_bytes>>>(
          d_input.data(), count, d_shared.data());
    };

    std::vector<unsigned int> global_output(kBinCount, 0U),
        shared_output(kBinCount, 0U);
    const auto run_checks = [&](const auto& expected, const char* distribution) {
      CUDA_CHECK(cudaMemset(d_global.data(), 0, d_global.bytes()));
      CUDA_CHECK(cudaMemset(d_shared.data(), 0, d_shared.bytes()));
      launch_global();
      launch_shared();
      CUDA_CHECK(cudaGetLastError());
      CUDA_CHECK(cudaDeviceSynchronize());
      d_global.copy_to(global_output);
      d_shared.copy_to(shared_output);
      const std::string global_label = std::string(distribution) + " global atomic";
      const std::string shared_label =
          std::string(distribution) + " shared privatized";
      const bool global_ok =
          check_histogram(expected, global_output, global_label.c_str());
      const bool shared_ok =
          check_histogram(expected, shared_output, shared_label.c_str());
      return global_ok && shared_ok;
    };
    if (!run_checks(full_range_expected, "full-range")) {
      std::cerr << "Do not time a histogram that fails exact bin counts.\n";
      return 2;
    }

    const auto contended_expected = fill_distribution(input, 64U);
    d_input.copy_from(input);
    if (!run_checks(contended_expected, "64-bin contended")) {
      std::cerr << "Do not time a histogram that fails under contention.\n";
      return 2;
    }
    CUDA_CHECK(cudaMemset(d_global.data(), 0, d_global.bytes()));
    CUDA_CHECK(cudaMemset(d_shared.data(), 0, d_shared.bytes()));

    // Timings use the validated 64-bin distribution. Repeated launches
    // accumulate counts, but the contention and instruction path are unchanged.
    const double global_ms = bench::kernel_median_ms(launch_global, 3, 10, 7);
    const double shared_ms = bench::kernel_median_ms(launch_shared, 3, 10, 7);
    int shared_active_blocks_per_sm = 0;
    CUDA_CHECK(cudaOccupancyMaxActiveBlocksPerMultiprocessor(
        &shared_active_blocks_per_sm, shared_histogram_kernel, threads,
        shared_bytes));
    const double theoretical_occupancy =
        static_cast<double>(shared_active_blocks_per_sm * threads) /
        properties.maxThreadsPerMultiProcessor;

    std::cout << "count=" << count << " benchmark_active_bins=64"
              << " blocks=" << blocks << '\n'
              << "global_atomic_kernel_median_ms=" << global_ms << '\n'
              << "shared_privatized_kernel_median_ms=" << shared_ms << '\n'
              << "kernel_speedup=" << global_ms / shared_ms << '\n'
              << "shared_active_blocks_per_sm=" << shared_active_blocks_per_sm
              << " theoretical_thread_occupancy=" << theoretical_occupancy << '\n';
    return 0;
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return 1;
  }
}
