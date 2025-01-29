#include "get_run_lengths.hpp"

namespace py = pybind11;

// Explicit instantiation for int16_t
py::array get_run_lengths_int16(py::array_t<int16_t> x) {
  return get_run_lengths_impl<int16_t>(x);
}

// Explicit instantiation for int32_t
py::array get_run_lengths_int32(py::array_t<int32_t> x) {
  return get_run_lengths_impl<int32_t>(x);
}

PYBIND11_MODULE(get_run_lengths_cpp_ext, m) {
  m.doc() = "C++ implementation of get_run_lengths using pybind11";
  m.def("get_run_lengths_int16", &get_run_lengths_int16,
        "Calculate run lengths of zeros and non-zeros in a signal (int16)");
  m.def("get_run_lengths_int32", &get_run_lengths_int32,
        "Calculate run lengths of zeros and non-zeros in a signal (int32)");
}
