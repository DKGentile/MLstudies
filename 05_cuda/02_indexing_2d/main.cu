#include "lab_support.cuh"

#include <climits>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <vector>

__global__ void affine_2d_kernel(const float* input, float* output, int width,
                                 int height) {
  // TODO(learner): Derive x and y from the 2-D grid, reject out-of-range
  // threads, flatten (y, x) in row-major order, and apply the formula in the
  // README. Keep x as the fastest-changing dimension for adjacent threads.
  (void)input;
  (void)output;
  (void)width;
  (void)height;
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

    std::vector<float> input(count), expected(count), actual(count, 0.0F);
    for (int y = 0; y < height; ++y) {
      for (int x = 0; x < width; ++x) {
        const std::size_t index = static_cast<std::size_t>(y) * width + x;
        input[index] = static_cast<float>((index * 17U + 5U) % 251U) / 251.0F;
        expected[index] = 1.25F * input[index] + 0.01F * y + 0.001F * x;
      }
    }

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
      affine_2d_kernel<<<blocks, threads>>>(d_input.data(), d_output.data(), width,
                                           height);
    };

    launch();
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());
    d_output.copy_to(actual);
    if (!lab::check_close(expected, actual, 2.0e-6, 2.0e-6)) {
      std::cerr << "Hint: check x/y bounds independently before flattening.\n";
      return 2;
    }

    const double kernel_ms = lab::median_kernel_ms(launch);
    std::cout << "shape=" << width << 'x' << height
              << " kernel_median_ms=" << kernel_ms << '\n';
    return 0;
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return 1;
  }
}
