#pragma once

#include <Eigen/Dense>
#include <cmath>
#include <iostream>
#include <pybind11/eigen.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

template <typename T>
std::tuple<py::array_t<float>, py::array_t<T>, py::array_t<T>>
markov_predict_impl(py::array_t<T> x, size_t M, size_t num_training_samples) {
  // Get array buffer
  auto x_buf = x.request();
  T *x_ptr = static_cast<T *>(x_buf.ptr);
  size_t N = x_buf.shape[0];

  // Keep initial values for reconstruction
  size_t initial_size = M - 1;
  std::vector<ssize_t> initial_shape = {static_cast<ssize_t>(initial_size)};
  py::array_t<T> initial(initial_shape);
  py::buffer_info initial_buf = initial.request(true);
  T *initial_ptr = static_cast<T *>(initial_buf.ptr);

  // Copy initial values
  for (size_t i = 0; i < initial_size; i++) {
    initial_ptr[i] = x_ptr[i];
  }

  // Create sequences matrix for linear regression
  size_t resid_size = N - M + 1;
  // Use only num_training_samples sequences for model fitting
  size_t num_samples_for_fit = std::min(resid_size, num_training_samples);
  // Take evenly spaced samples for training
  size_t stride =
      resid_size > num_training_samples ? resid_size / num_training_samples : 1;

  Eigen::MatrixXf predictors(num_samples_for_fit, M - 1);
  Eigen::VectorXf target(num_samples_for_fit);

  // Fill predictors matrix and target vector with strided training samples
  for (size_t i = 0; i < num_samples_for_fit; i++) {
    size_t idx = i * stride;
    for (size_t j = 0; j < M - 1; j++) {
      predictors(i, j) = static_cast<float>(x_ptr[idx + j]);
    }
    target(i) = static_cast<float>(x_ptr[idx + M - 1]);
  }

  // Add constant term column (ones) to predictors
  Eigen::MatrixXf X(predictors.rows(), predictors.cols() + 1);
  X << predictors, Eigen::VectorXf::Ones(predictors.rows());

  // Solve least squares problem: X * coeffs = target
  Eigen::VectorXf coeffs = X.colPivHouseholderQr().solve(target);

  // Create coefficients array
  std::vector<ssize_t> coeffs_shape = {static_cast<ssize_t>(M)};
  py::array_t<float> coeffs_array(coeffs_shape);
  py::buffer_info coeffs_buf = coeffs_array.request(true);
  float *coeffs_ptr = static_cast<float *>(coeffs_buf.ptr);

  // Copy coefficients
  for (size_t i = 0; i < M - 1; i++) {
    coeffs_ptr[i] = coeffs(i);
  }
  coeffs_ptr[M - 1] = coeffs(M - 1); // bias term

  // Calculate residuals
  std::vector<ssize_t> resid_shape = {static_cast<ssize_t>(resid_size)};
  py::array_t<T> residuals(resid_shape);
  py::buffer_info resid_buf = residuals.request(true);
  T *resid_ptr = static_cast<T *>(resid_buf.ptr);

  for (size_t i = 0; i < resid_size; i++) {
    float prediction = 0.0f;
    for (size_t j = 0; j < M - 1; j++) {
      float term = coeffs_ptr[j] * static_cast<float>(x_ptr[i + j]);
      prediction += term;
    }
    prediction += coeffs_ptr[M - 1]; // bias term
    float rounded_prediction = std::round(prediction);
    resid_ptr[i] = x_ptr[i + M - 1] - static_cast<T>(rounded_prediction);
  }

  return std::make_tuple(coeffs_array, initial, residuals);
}
