cmake_minimum_required(VERSION 3.15)
project(markov_cpp)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

# Fetch and include pybind11
include(FetchContent)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v2.11.1
)

# Fetch and include Eigen
FetchContent_Declare(
    eigen
    GIT_REPOSITORY https://gitlab.com/libeigen/eigen.git
    GIT_TAG 3.4.0
)

FetchContent_MakeAvailable(pybind11 eigen)

# Build markov_reconstruct module
pybind11_add_module(markov_reconstruct_cpp_ext markov_reconstruct.cpp)

# Build markov_predict module
pybind11_add_module(markov_predict_cpp_ext markov_predict.cpp)
target_link_libraries(markov_predict_cpp_ext PRIVATE Eigen3::Eigen)

# Install both modules
install(TARGETS markov_reconstruct_cpp_ext markov_predict_cpp_ext
        DESTINATION benchcompress/algorithms/simple_ans)
