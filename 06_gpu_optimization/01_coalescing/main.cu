#include "benchmark.cuh"

#include <climits>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <vector>

constexpr float kScale = 1.0009765625F;

__global__ void row_major_copy_kernel(const float* input, float* output,
                                      int width, int height) {
  const int x = static_cast<int>(blockIdx.x * blockDim.x + threadIdx.x);
  const int y = static_cast<int>(blockIdx.y);
  if (x < width && y < height) {
    const std::size_t index = static_cast<std::size_t>(y) * width + x;
    output[index] = input[index] * kScale;
  }
}

__global__ void column_order_copy_kernel(const float* input, float* output,
                                         int width, int height) {
  const int x = static_cast<int>(blockIdx.x);
  const int y = static_cast<int>(blockIdx.y * blockDim.y + threadIdx.y);
  if (x < width && y < height) {
    const std::size_t index = static_cast<std::size_t>(y) * width + x;
    output[index] = input[index] * kScale;
  }
}

int main(int argc, char** argv) {
  try {
    const std::size_t width_value =
        bench::parse_size_or(argc > 1 ? argv[1] : nullptr, 4096);
    const std::size_t height_value =
        bench::parse_size_or(argc > 2 ? argv[2] : nullptr, 2048);
    if (width_value > static_cast<std::size_t>(INT_MAX) ||
        height_value > static_cast<std::size_t>(INT_MAX) ||
        width_value > SIZE_MAX / height_value) {
      throw std::invalid_argument("matrix dimensions are too large");
    }
    const int width = static_cast<int>(width_value);
    const int height = static_cast<int>(height_value);
    const std::size_t count = width_value * height_value;
    const cudaDeviceProp properties = bench::print_device_summary();
    if (width > properties.maxGridSize[0] || height > properties.maxGridSize[1]) {
      throw std::invalid_argument(
          "dimensions exceed the 2-D grid limits used by this experiment");
    }

    std::vector<float> input(count), expected(count), row_output(count, 0.0F),
        column_output(count, 0.0F);
    for (std::size_t i = 0; i < count; ++i) {
      input[i] = static_cast<float>(i % 1021U) / 1021.0F;
      expected[i] = input[i] * kScale;
    }

    bench::DeviceBuffer<float> d_input(count), d_row(count), d_column(count);
    d_input.copy_from(input);
    const dim3 row_threads(256, 1);
    const dim3 row_blocks((width + row_threads.x - 1) / row_threads.x, height);
    const dim3 column_threads(1, 256);
    const dim3 column_blocks(width,
                             (height + column_threads.y - 1) / column_threads.y);
    const auto launch_row = [&] {
      row_major_copy_kernel<<<row_blocks, row_threads>>>(
          d_input.data(), d_row.data(), width, height);
    };
    const auto launch_column = [&] {
      column_order_copy_kernel<<<column_blocks, column_threads>>>(
          d_input.data(), d_column.data(), width, height);
    };

    launch_row();
    launch_column();
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());
    d_row.copy_to(row_output);
    d_column.copy_to(column_output);
    const bool row_ok =
        bench::check_close(expected, row_output, 0.0, 0.0, "row-major");
    const bool column_ok =
        bench::check_close(expected, column_output, 0.0, 0.0, "column-order");
    if (!row_ok || !column_ok) {
      return 2;
    }

    const double row_ms = bench::kernel_median_ms(launch_row);
    const double column_ms = bench::kernel_median_ms(launch_column);
    const double bytes = static_cast<double>(count) * 2.0 * sizeof(float);
    std::cout << "shape=" << width << 'x' << height << '\n'
              << "row_major_ms=" << row_ms
              << " effective_GB_per_s=" << bytes / (row_ms * 1.0e6) << '\n'
              << "column_order_ms=" << column_ms
              << " effective_GB_per_s=" << bytes / (column_ms * 1.0e6) << '\n'
              << "row_over_column_speedup=" << column_ms / row_ms << '\n';

    // TODO(learner): Copy both timing rows and the matching Nsight memory
    // metrics into results/BENCHMARK_TEMPLATE.md before drawing a conclusion.
    return 0;
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return 1;
  }
}
