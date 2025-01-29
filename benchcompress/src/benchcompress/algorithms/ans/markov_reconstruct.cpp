#include "markov_reconstruct.hpp"

namespace py = pybind11;

// Explicit instantiation for int16_t
py::array_t<int16_t> markov_reconstruct_int16(py::array_t<float> coeffs,
                                              py::array_t<int16_t> initial,
                                              py::array_t<int16_t> resid) {
  return markov_reconstruct_impl<int16_t>(coeffs, initial, resid);
}

// Explicit instantiation for int32_t
py::array_t<int32_t> markov_reconstruct_int32(py::array_t<float> coeffs,
                                              py::array_t<int32_t> initial,
                                              py::array_t<int32_t> resid) {
  return markov_reconstruct_impl<int32_t>(coeffs, initial, resid);
}

PYBIND11_MODULE(markov_reconstruct_cpp_ext, m) {
  m.doc() = "C++ implementation of markov_reconstruct using pybind11";
  m.def("markov_reconstruct_int16", &markov_reconstruct_int16,
        "Reconstruct signal from Markov model parameters and residuals (int16)",
        py::arg("coeffs"), py::arg("initial"), py::arg("resid"));
  m.def("markov_reconstruct_int32", &markov_reconstruct_int32,
        "Reconstruct signal from Markov model parameters and residuals (int32)",
        py::arg("coeffs"), py::arg("initial"), py::arg("resid"));
}
