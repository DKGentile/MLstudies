#include "lab_support.cuh"

#include <climits>
#include <cstddef>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <vector>

__global__ void reduce_blocks_kernel(const float* input, float* partial_sums,
                                     std::size_t n) {
  extern __shared__ float scratch[];

  // TODO(learner): Load up to two input values per thread into scratch, reduce
  // scratch cooperatively to one value, and let thread 0 write this block's
  // result. Barriers must be reached by every thread in the block.
  (void)input;
  (void)partial_sums;
  (void)n;
  (void)scratch;
}

int main(int argc, char** argv) {
  try {
    const std::size_t n = lab::parse_size_or(argc > 1 ? argv[1] : nullptr,
                                             (1U << 20U) + 13U);
    const cudaDeviceProp properties = lab::print_device_summary();

    std::vector<float> input(n);
    for (std::size_t i = 0; i < n; ++i) {
      // Positive, exactly representable values ensure dropped chunks cannot
      // cancel to zero and accidentally satisfy the scalar checksum.
      input[i] = static_cast<float>((i % 7U) + 1U);
    }
    const double expected = std::accumulate(input.begin(), input.end(), 0.0);

    constexpr int threads = 256;
    const std::size_t block_count =
        (n + (2 * threads) - 1) / (2 * threads);
    if (block_count > static_cast<std::size_t>(properties.maxGridSize[0]) ||
        block_count > static_cast<std::size_t>(INT_MAX)) {
      throw std::invalid_argument("input requires more reduction blocks than this GPU supports");
    }
    const int blocks = static_cast<int>(block_count);
    std::vector<float> partial_sums(static_cast<std::size_t>(blocks), 0.0F);
    lab::DeviceBuffer<float> d_input(n), d_partial(partial_sums.size());
    d_input.copy_from(input);
    CUDA_CHECK(cudaMemset(d_partial.data(), 0, d_partial.bytes()));

    const auto launch = [&] {
      reduce_blocks_kernel<<<blocks, threads, threads * sizeof(float)>>>(
          d_input.data(), d_partial.data(), n);
    };

    launch();
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());
    d_partial.copy_to(partial_sums);
    const double actual =
        std::accumulate(partial_sums.begin(), partial_sums.end(), 0.0);
    const double error = std::abs(expected - actual);
    if (!std::isfinite(actual) || error > 1.0e-3) {
      std::cerr << std::setprecision(10) << "FAIL: expected sum=" << expected
                << " actual=" << actual << " abs_error=" << error << '\n'
                << "Hint: initialize inactive lanes and inspect the final partial block.\n";
      return 2;
    }
    std::cout << "PASS: sum=" << actual << " from " << blocks
              << " block partials\n";

    const double kernel_ms = lab::median_kernel_ms(launch);
    std::cout << "n=" << n << " kernel_median_ms=" << kernel_ms << '\n';
    return 0;
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return 1;
  }
}
