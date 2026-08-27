#include "lab_support.cuh"

#include <algorithm>
#include <climits>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <vector>

constexpr int kRadius = 2;
constexpr int kDiameter = 2 * kRadius + 1;

__global__ void box_blur_kernel(const float* input, float* output, int width,
                                int height) {
  // TODO(learner): Map one thread to one output pixel. Sum the clamped 5 x 5
  // neighborhood in global memory and write its average. Do not special-case
  // the benchmark dimensions.
  (void)input;
  (void)output;
  (void)width;
  (void)height;
}

std::vector<float> cpu_box_blur(const std::vector<float>& input, int width,
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
        lab::parse_size_or(argc > 1 ? argv[1] : nullptr, 641);
    const std::size_t height_value =
        lab::parse_size_or(argc > 2 ? argv[2] : nullptr, 479);
    if (width_value > static_cast<std::size_t>(INT_MAX) ||
        height_value > static_cast<std::size_t>(INT_MAX) ||
        width_value > SIZE_MAX / height_value) {
      throw std::invalid_argument("image dimensions are too large");
    }
    const int width = static_cast<int>(width_value);
    const int height = static_cast<int>(height_value);
    const std::size_t count = width_value * height_value;
    const cudaDeviceProp properties = lab::print_device_summary();

    std::vector<float> input(count), actual(count, 0.0F);
    for (std::size_t i = 0; i < count; ++i) {
      input[i] = static_cast<float>((i * 29U + i / 11U + 7U) % 1021U) / 1021.0F;
    }
    const std::vector<float> expected = cpu_box_blur(input, width, height);

    lab::DeviceBuffer<float> d_input(count), d_output(count);
    d_input.copy_from(input);
    CUDA_CHECK(cudaMemset(d_output.data(), 0, d_output.bytes()));

    const dim3 threads(16, 16);
    const std::size_t grid_x = (width_value + threads.x - 1) / threads.x;
    const std::size_t grid_y = (height_value + threads.y - 1) / threads.y;
    if (grid_x > static_cast<std::size_t>(properties.maxGridSize[0]) ||
        grid_y > static_cast<std::size_t>(properties.maxGridSize[1])) {
      throw std::invalid_argument("image requires a grid larger than this GPU supports");
    }
    const dim3 blocks(static_cast<unsigned int>(grid_x),
                      static_cast<unsigned int>(grid_y));
    const auto launch = [&] {
      box_blur_kernel<<<blocks, threads>>>(d_input.data(), d_output.data(), width,
                                          height);
    };

    launch();
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());
    d_output.copy_to(actual);
    if (!lab::check_close(expected, actual, 2.0e-5, 2.0e-5)) {
      std::cerr << "Hint: make the CPU and GPU edge-clamping rules identical.\n";
      return 2;
    }

    const double kernel_ms = lab::median_kernel_ms(launch, 5, 20, 7);
    std::cout << "shape=" << width << 'x' << height
              << " radius=" << kRadius << " kernel_median_ms=" << kernel_ms
              << '\n';
    return 0;
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return 1;
  }
}
