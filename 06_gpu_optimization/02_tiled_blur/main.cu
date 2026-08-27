#include "benchmark.cuh"

#include <algorithm>
#include <climits>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <vector>

constexpr int kRadius = 2;
constexpr int kDiameter = 2 * kRadius + 1;

__device__ __forceinline__ int clamp_device(int value, int low, int high) {
  return value < low ? low : (value > high ? high : value);
}

__global__ void naive_blur_kernel(const float* input, float* output, int width,
                                  int height) {
  const int x = static_cast<int>(blockIdx.x * blockDim.x + threadIdx.x);
  const int y = static_cast<int>(blockIdx.y * blockDim.y + threadIdx.y);
  if (x >= width || y >= height) {
    return;
  }

  float sum = 0.0F;
  for (int dy = -kRadius; dy <= kRadius; ++dy) {
    const int sample_y = clamp_device(y + dy, 0, height - 1);
    for (int dx = -kRadius; dx <= kRadius; ++dx) {
      const int sample_x = clamp_device(x + dx, 0, width - 1);
      sum += input[static_cast<std::size_t>(sample_y) * width + sample_x];
    }
  }
  output[static_cast<std::size_t>(y) * width + x] =
      sum / static_cast<float>(kDiameter * kDiameter);
}

__global__ void tiled_blur_kernel(const float* input, float* output, int width,
                                  int height) {
  extern __shared__ float tile[];

  // TODO(learner):
  // 1. Cooperatively load the block footprint and radius-2 halo. Flatten
  //    threadIdx to let all threads cover a tile larger than the block.
  // 2. Clamp global load coordinates to match the CPU boundary policy.
  // 3. Synchronize every thread in the block after the tile is populated.
  // 4. For in-range outputs only, compute the 5 x 5 average from tile and store.
  // Derive the shared row stride from blockDim.x; do not hard-code image sizes.
  (void)input;
  (void)output;
  (void)width;
  (void)height;
  (void)tile;
}

std::vector<float> cpu_blur(const std::vector<float>& input, int width,
                            int height) {
  std::vector<float> output(input.size(), 0.0F);
  for (int y = 0; y < height; ++y) {
    for (int x = 0; x < width; ++x) {
      float sum = 0.0F;
      for (int dy = -kRadius; dy <= kRadius; ++dy) {
        const int sample_y = std::clamp(y + dy, 0, height - 1);
        for (int dx = -kRadius; dx <= kRadius; ++dx) {
          const int sample_x = std::clamp(x + dx, 0, width - 1);
          sum += input[static_cast<std::size_t>(sample_y) * width + sample_x];
        }
      }
      output[static_cast<std::size_t>(y) * width + x] =
          sum / static_cast<float>(kDiameter * kDiameter);
    }
  }
  return output;
}

int main(int argc, char** argv) {
  try {
    const std::size_t width_value =
        bench::parse_size_or(argc > 1 ? argv[1] : nullptr, 1921);
    const std::size_t height_value =
        bench::parse_size_or(argc > 2 ? argv[2] : nullptr, 1081);
    if (width_value > static_cast<std::size_t>(INT_MAX) ||
        height_value > static_cast<std::size_t>(INT_MAX) ||
        width_value > SIZE_MAX / height_value) {
      throw std::invalid_argument("image dimensions are too large");
    }
    const int width = static_cast<int>(width_value);
    const int height = static_cast<int>(height_value);
    const std::size_t count = width_value * height_value;
    const cudaDeviceProp properties = bench::print_device_summary();

    std::vector<float> input(count), expected, naive_output(count, 0.0F),
        tiled_output(count, 0.0F);
    for (std::size_t i = 0; i < count; ++i) {
      input[i] = static_cast<float>((i * 29U + i / 11U + 7U) % 1021U) / 1021.0F;
    }
    double cpu_ms = 0.0;
    cpu_ms = bench::wall_median_ms([&] { expected = cpu_blur(input, width, height); },
                                   0, 3);

    bench::DeviceBuffer<float> d_input(count), d_naive(count), d_tiled(count);
    d_input.copy_from(input);
    CUDA_CHECK(cudaMemset(d_naive.data(), 0, d_naive.bytes()));
    CUDA_CHECK(cudaMemset(d_tiled.data(), 0, d_tiled.bytes()));

    const dim3 threads(32, 8);
    const std::size_t grid_x = (width_value + threads.x - 1) / threads.x;
    const std::size_t grid_y = (height_value + threads.y - 1) / threads.y;
    if (grid_x > static_cast<std::size_t>(properties.maxGridSize[0]) ||
        grid_y > static_cast<std::size_t>(properties.maxGridSize[1])) {
      throw std::invalid_argument("image requires a grid larger than this GPU supports");
    }
    const dim3 blocks(static_cast<unsigned int>(grid_x),
                      static_cast<unsigned int>(grid_y));
    const std::size_t tile_width = threads.x + 2 * kRadius;
    const std::size_t tile_height = threads.y + 2 * kRadius;
    const std::size_t shared_bytes = tile_width * tile_height * sizeof(float);

    const auto launch_naive = [&] {
      naive_blur_kernel<<<blocks, threads>>>(d_input.data(), d_naive.data(), width,
                                            height);
    };
    const auto launch_tiled = [&] {
      tiled_blur_kernel<<<blocks, threads, shared_bytes>>>(
          d_input.data(), d_tiled.data(), width, height);
    };

    launch_naive();
    launch_tiled();
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());
    d_naive.copy_to(naive_output);
    d_tiled.copy_to(tiled_output);
    const bool naive_ok =
        bench::check_close(expected, naive_output, 2.0e-5, 2.0e-5, "naive blur");
    const bool tiled_ok =
        bench::check_close(expected, tiled_output, 2.0e-5, 2.0e-5, "tiled blur");
    if (!naive_ok || !tiled_ok) {
      std::cerr << "Do not benchmark or profile the optimized kernel until both checks pass.\n";
      return 2;
    }

    const double naive_ms = bench::kernel_median_ms(launch_naive, 5, 20, 7);
    const double tiled_ms = bench::kernel_median_ms(launch_tiled, 5, 20, 7);
    const double tiled_end_to_end_ms = bench::wall_median_ms(
        [&] {
          d_input.copy_from(input);
          launch_tiled();
          CUDA_CHECK(cudaGetLastError());
          d_tiled.copy_to(tiled_output);
        },
        2, 7);

    int active_blocks_per_sm = 0;
    CUDA_CHECK(cudaOccupancyMaxActiveBlocksPerMultiprocessor(
        &active_blocks_per_sm, tiled_blur_kernel,
        static_cast<int>(threads.x * threads.y), shared_bytes));
    const double theoretical_occupancy =
        static_cast<double>(active_blocks_per_sm * threads.x * threads.y) /
        properties.maxThreadsPerMultiProcessor;

    std::cout << "shape=" << width << 'x' << height
              << " shared_bytes_per_block=" << shared_bytes << '\n'
              << "cpu_wall_median_ms=" << cpu_ms << '\n'
              << "naive_kernel_median_ms=" << naive_ms << '\n'
              << "tiled_kernel_median_ms=" << tiled_ms << '\n'
              << "tiled_end_to_end_median_ms=" << tiled_end_to_end_ms << '\n'
              << "kernel_speedup=" << naive_ms / tiled_ms << '\n'
              << "occupancy_api_active_blocks_per_sm=" << active_blocks_per_sm
              << " theoretical_thread_occupancy=" << theoretical_occupancy << '\n';
    return 0;
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return 1;
  }
}
