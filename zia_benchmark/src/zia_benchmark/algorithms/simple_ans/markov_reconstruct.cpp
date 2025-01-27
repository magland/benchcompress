#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>
#include <iostream>

namespace py = pybind11;

py::array_t<int16_t> markov_reconstruct_cpp(
    py::array_t<float> coeffs,
    py::array_t<int16_t> initial,
    py::array_t<int16_t> resid
) {
    // Get array buffers
    auto coeffs_buf = coeffs.request();
    auto initial_buf = initial.request();
    auto resid_buf = resid.request();

    // Get raw pointers to data
    float* coeffs_ptr = static_cast<float*>(coeffs_buf.ptr);
    int16_t* initial_ptr = static_cast<int16_t*>(initial_buf.ptr);
    int16_t* resid_ptr = static_cast<int16_t*>(resid_buf.ptr);

    // Calculate dimensions
    size_t M = initial_buf.shape[0] + 1;  // Number of samples used in prediction
    size_t output_size = resid_buf.shape[0] + initial_buf.shape[0];

    // Create output array with explicit shape and memory ownership
    std::vector<ssize_t> shape = {static_cast<ssize_t>(output_size)};
    py::array_t<int16_t> output(shape);
    py::buffer_info output_buf = output.request(true); // Request writable buffer
    int16_t* output_ptr = static_cast<int16_t*>(output_buf.ptr);

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
        int16_t final_value = static_cast<int16_t>(rounded_prediction + static_cast<float>(resid_ptr[i]));
        output_ptr[i + M - 1] = final_value;
    }

    return output;
}

PYBIND11_MODULE(markov_reconstruct_cpp_ext, m) {
    m.doc() = "C++ implementation of markov_reconstruct using pybind11";
    m.def("markov_reconstruct_cpp", &markov_reconstruct_cpp,
          "Reconstruct signal from Markov model parameters and residuals",
          py::arg("coeffs"), py::arg("initial"), py::arg("resid"));
}
