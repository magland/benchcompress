cmake_minimum_required(VERSION 3.15)
project(markov_reconstruct_cpp)

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
FetchContent_MakeAvailable(pybind11)

pybind11_add_module(markov_reconstruct_cpp_ext markov_reconstruct.cpp)

install(TARGETS markov_reconstruct_cpp_ext DESTINATION zia_benchmark/algorithms/simple_ans)
