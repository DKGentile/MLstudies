#include "lab_support.cuh"

#include <array>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <vector>

constexpr int kBinCount = 256;

__global__ void histogram_kernel(const std::uint8_t* input, std::size_t n,
                                 unsigned int* bins) {
  // TODO(learner): Walk the input with a grid-stride loop and atomically update
  // the bin selected by each byte. The harness owns bin initialization.
  (void)input;
  (void)n;
  (void)bins;
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

bool check_histogram(const std::array<unsigned int, kBinCount>& expected,
                     const std::vector<unsigned int>& actual,
                     const char* label) {
  std::size_t mismatches = 0;
  for (int bin = 0; bin < kBinCount; ++bin) {
    if (actual[bin] != expected[bin]) {
      if (mismatches < 5) {
        std::cerr << label << " bin=" << bin << " expected=" << expected[bin]
                  << " actual=" << actual[bin] << '\n';
      }
      ++mismatches;
    }
  }
  if (mismatches != 0) {
    std::cerr << "FAIL: " << label << " mismatched_bins=" << mismatches << '\n';
    return false;
  }
  std::cout << "PASS: " << label << " all bins match\n";
  return true;
}

int main(int argc, char** argv) {
  try {
    const std::size_t n = lab::parse_size_or(argc > 1 ? argv[1] : nullptr,
                                             (1U << 22U) + 19U);
    lab::print_device_summary();

    std::vector<std::uint8_t> input(n);
    const auto full_range_expected = fill_distribution(input, kBinCount);

    lab::DeviceBuffer<std::uint8_t> d_input(n);
    lab::DeviceBuffer<unsigned int> d_bins(kBinCount);
    d_input.copy_from(input);

    constexpr int threads = 256;
    constexpr int blocks = 256;
    const auto launch = [&] {
      histogram_kernel<<<blocks, threads>>>(d_input.data(), n, d_bins.data());
    };

    std::vector<unsigned int> actual(kBinCount, 0U);
    const auto run_check = [&](const auto& expected, const char* label) {
      CUDA_CHECK(cudaMemset(d_bins.data(), 0, d_bins.bytes()));
      launch();
      CUDA_CHECK(cudaGetLastError());
      CUDA_CHECK(cudaDeviceSynchronize());
      d_bins.copy_to(actual);
      return check_histogram(expected, actual, label);
    };
    if (!run_check(full_range_expected, "full-range distribution")) {
      std::cerr << "Hint: every uint8 value must select its own bin.\n";
      return 2;
    }

    const auto contended_expected = fill_distribution(input, 64U);
    d_input.copy_from(input);
    if (!run_check(contended_expected, "64-bin contended distribution")) {
      std::cerr << "Hint: one input byte means one atomic increment.\n";
      return 2;
    }
    CUDA_CHECK(cudaMemset(d_bins.data(), 0, d_bins.bytes()));

    // The timed dataset uses 64 active bins. Repeated launches accumulate more
    // counts, but the contention and instruction path remain representative.
    const double kernel_ms = lab::median_kernel_ms(launch, 3, 10, 7);
    std::cout << "n=" << n << " benchmark_active_bins=64"
              << " kernel_median_ms=" << kernel_ms
              << " input_GB_per_s="
              << static_cast<double>(n) / (kernel_ms * 1.0e6) << '\n';
    return 0;
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return 1;
  }
}
