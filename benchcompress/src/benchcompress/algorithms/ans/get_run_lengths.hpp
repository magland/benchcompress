#pragma once

#include <cstdint>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <vector>

namespace py = pybind11;

template <typename T> py::array get_run_lengths_impl(py::array_t<T> x) {
  auto x_buf = x.request();
  T *x_ptr = static_cast<T *>(x_buf.ptr);
  size_t N = x_buf.shape[0];

  std::vector<uint32_t> runs;
  size_t i = 0;
  uint32_t current_nonzero_run_length = 0;

  while (i < N) {
    // Check for a sequence of at least 10 zeros
    bool has_zeros = true;
    for (size_t j = 0; j < 10 && i + j < N; j++) {
      if (x_ptr[i + j] != 0) {
        has_zeros = false;
        break;
      }
    }

    if (has_zeros) {
      // Add current non-zero run if any
      runs.push_back(current_nonzero_run_length);
      current_nonzero_run_length = 0;

      // Count consecutive zeros
      size_t j = i;
      while (j < N && x_ptr[j] == 0) {
        j++;
      }
      runs.push_back(j - i);
      i = j;
    } else {
      current_nonzero_run_length++;
      i++;
    }
  }

  // Add final non-zero run if any
  if (current_nonzero_run_length > 0) {
    runs.push_back(current_nonzero_run_length);
  }

  // Determine appropriate dtype based on max run length
  uint32_t max_run = 0;
  for (const auto &run : runs) {
    if (run > max_run) {
      max_run = run;
    }
  }

  // Create numpy array with appropriate dtype
  std::vector<ssize_t> shape = {static_cast<ssize_t>(runs.size())};

  if (max_run < 256) {
    py::array_t<uint8_t> result(shape);
    auto result_buf = result.request();
    uint8_t *result_ptr = static_cast<uint8_t *>(result_buf.ptr);
    for (size_t i = 0; i < runs.size(); i++) {
      result_ptr[i] = static_cast<uint8_t>(runs[i]);
    }
    return result;
  } else if (max_run < 65536) {
    py::array_t<uint16_t> result(shape);
    auto result_buf = result.request();
    uint16_t *result_ptr = static_cast<uint16_t *>(result_buf.ptr);
    for (size_t i = 0; i < runs.size(); i++) {
      result_ptr[i] = static_cast<uint16_t>(runs[i]);
    }
    return result;
  } else {
    py::array_t<uint32_t> result(shape);
    auto result_buf = result.request();
    uint32_t *result_ptr = static_cast<uint32_t *>(result_buf.ptr);
    for (size_t i = 0; i < runs.size(); i++) {
      result_ptr[i] = runs[i];
    }
    return result;
  }
}
