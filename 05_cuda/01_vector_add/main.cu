#include "lab_support.cuh"

#include <cmath>
#include <cstddef>
#include <iostream>
#include <vector>

__global__ void vector_add_kernel(const float* a, const float* b, float* out,
                                  std::size_t n) {
  // TODO(learner): Compute a global index and grid-wide stride, then add every
  // element owned by this thread. Guard all accesses with i < n.
  (void)a;
  (void)b;
  (void)out;
  (void)n;
}

int main(int argc, char** argv) {
  try {
    const std::size_t n = lab::parse_size_or(argc > 1 ? argv[1] : nullptr,
                                             (1U << 20U) + 7U);
    lab::print_device_summary();

    std::vector<float> a(n), b(n), expected(n), actual(n, 0.0F);
    for (std::size_t i = 0; i < n; ++i) {
      a[i] = std::sin(static_cast<float>(i) * 0.001F);
      b[i] = std::cos(static_cast<float>(i) * 0.002F);
      expected[i] = a[i] + b[i];
    }

    lab::DeviceBuffer<float> d_a(n), d_b(n), d_out(n);
    d_a.copy_from(a);
    d_b.copy_from(b);
    CUDA_CHECK(cudaMemset(d_out.data(), 0, d_out.bytes()));

    constexpr int threads = 256;
    constexpr std::size_t kMaxBlocks = 256;
    const std::size_t blocks_needed = (n + threads - 1) / threads;
    const int blocks = static_cast<int>(std::min(blocks_needed, kMaxBlocks));
    const auto launch = [&] {
      vector_add_kernel<<<blocks, threads>>>(d_a.data(), d_b.data(), d_out.data(), n);
    };

    launch();
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());
    d_out.copy_to(actual);
    if (!lab::check_close(expected, actual, 1.0e-6, 1.0e-6)) {
      std::cerr << "Hint: inspect the last partial block and your grid stride.\n";
      return 2;
    }

    const double kernel_ms = lab::median_kernel_ms(launch);
    const double bytes = static_cast<double>(n) * 3.0 * sizeof(float);
    std::cout << "n=" << n << " kernel_median_ms=" << kernel_ms
              << " estimated_GB_per_s=" << bytes / (kernel_ms * 1.0e6) << '\n';
    return 0;
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return 1;
  }
}
