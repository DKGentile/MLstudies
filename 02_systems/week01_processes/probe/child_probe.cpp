#include <cstdlib>
#include <exception>
#include <iostream>
#include <string>

int main(int argc, char** argv) {
  if (argc != 3) {
    std::cerr << "usage: child_probe --exit CODE | --echo TEXT\n";
    return 64;
  }

  const std::string mode = argv[1];
  const std::string value = argv[2];

  if (mode == "--echo") {
    std::cout << "probe-out:" << value << '\n';
    return 0;
  }

  if (mode == "--exit") {
    try {
      const int code = std::stoi(value);
      if (code < 0 || code > 127) {
        std::cerr << "exit code must be in [0, 127]\n";
        return 64;
      }
      std::cout << "probe-out:" << code << '\n';
      std::cerr << "probe-err:" << code << '\n';
      return code;
    } catch (const std::exception&) {
      std::cerr << "invalid exit code\n";
      return 64;
    }
  }

  std::cerr << "unknown mode\n";
  return 64;
}

