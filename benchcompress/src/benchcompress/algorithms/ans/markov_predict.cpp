#include "markov_predict.hpp"

namespace py = pybind11;

// Explicit instantiation for int16_t
std::tuple<py::array_t<float>, py::array_t<int16_t>, py::array_t<int16_t>>
markov_predict_int16(py::array_t<int16_t> x, size_t M,
                     size_t num_training_samples) {
  return markov_predict_impl<int16_t>(x, M, num_training_samples);
}

// Explicit instantiation for int32_t
std::tuple<py::array_t<float>, py::array_t<int32_t>, py::array_t<int32_t>>
markov_predict_int32(py::array_t<int32_t> x, size_t M,
                     size_t num_training_samples) {
  return markov_predict_impl<int32_t>(x, M, num_training_samples);
}

PYBIND11_MODULE(markov_predict_cpp_ext, m) {
  m.doc() = "C++ implementation of markov_predict using pybind11";
  m.def("markov_predict_int16", &markov_predict_int16,
        "Predict signal using Markov model and return coefficients, initial "
        "values and residuals (int16)",
        py::arg("x"), py::arg("M"), py::arg("num_training_samples") = 10000);
  m.def("markov_predict_int32", &markov_predict_int32,
        "Predict signal using Markov model and return coefficients, initial "
        "values and residuals (int32)",
        py::arg("x"), py::arg("M"), py::arg("num_training_samples") = 10000);
}
