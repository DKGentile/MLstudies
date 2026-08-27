#include <filesystem>
#include <iostream>
#include <stdexcept>
#include <string>

struct Options {
    std::filesystem::path engine;
    std::filesystem::path input;
};

Options parse_args(int argc, char** argv) {
    if (argc != 3) {
        throw std::invalid_argument("usage: edge_infer <model.engine> <video-or-image>");
    }
    return {argv[1], argv[2]};
}

int run_pipeline(const Options& options) {
    // LEARNER TODO: create a version-specific runtime adapter, validate tensor
    // contracts, run the decode/preprocess/infer/postprocess/track loop, and emit
    // stage timings. Keep allocations out of the per-frame loop.
    std::cerr << "pipeline not implemented\n"
              << "engine: " << options.engine << '\n'
              << "input:  " << options.input << '\n';
    return 2;
}

int main(int argc, char** argv) {
    try {
        return run_pipeline(parse_args(argc, argv));
    } catch (const std::exception& error) {
        std::cerr << "error: " << error.what() << '\n';
        return 1;
    }
}

