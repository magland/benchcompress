#pragma once

#include <cmath>
#include <iostream>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

template <typename T>
py::array_t<T> markov_reconstruct_impl(py::array_t<float> coeffs,
                                       py::array_t<T> initial,
                                       py::array_t<T> resid) {
  // Get array buffers
  auto coeffs_buf = coeffs.request();
  auto initial_buf = initial.request();
  auto resid_buf = resid.request();

  // Get raw pointers to data
  float *coeffs_ptr = static_cast<float *>(coeffs_buf.ptr);
  T *initial_ptr = static_cast<T *>(initial_buf.ptr);
  T *resid_ptr = static_cast<T *>(resid_buf.ptr);

  // Calculate dimensions
  size_t M = initial_buf.shape[0] + 1; // Number of samples used in prediction
  size_t output_size = resid_buf.shape[0] + initial_buf.shape[0];

  // Create output array with explicit shape and memory ownership
  std::vector<ssize_t> shape = {static_cast<ssize_t>(output_size)};
  py::array_t<T> output(shape);
  py::buffer_info output_buf = output.request(true); // Request writable buffer
  T *output_ptr = static_cast<T *>(output_buf.ptr);

  // Copy initial values with bounds check
  for (size_t i = 0; i < initial_buf.shape[0] && i < output_size; i++) {
    output_ptr[i] = initial_ptr[i];
  }

  size_t resid_size = resid_buf.shape[0];

  // Reconstruct signal iteratively
  for (size_t i = 0; i < resid_size; i++) {
    float prediction = 0.0f;

    // Calculate prediction using coefficients (excluding bias term)
    for (size_t j = 0; j < M - 1; j++) {
      float term = coeffs_ptr[j] * static_cast<float>(output_ptr[i + j]);
      prediction += term;
    }

    // Add bias term separately
    prediction += coeffs_ptr[coeffs_buf.shape[0] - 1];

    // Round prediction to nearest integer
    float rounded_prediction = std::round(prediction);

    // Add residual and store result
    T final_value =
        static_cast<T>(rounded_prediction + static_cast<float>(resid_ptr[i]));
    output_ptr[i + M - 1] = final_value;
  }

  return output;
}
