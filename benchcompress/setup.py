from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
from setuptools import Extension
import os
import sys
import subprocess

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(build_ext):
    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}"
        ]

        build_args = []

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp)
        subprocess.check_call(["cmake", "--build", "."] + build_args, cwd=self.build_temp)

setup(
    name="benchcompress",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "scipy",
        "zstandard",
        "simple_ans",
        "requests",
        "lindi",
        "brotli",
        "click",
        "pybind11>=2.11.1"
    ],
    ext_modules=[
        CMakeExtension("benchcompress.algorithms.ans.markov_reconstruct_cpp_ext",
                      sourcedir="src/benchcompress/algorithms/ans"),
        CMakeExtension("benchcompress.algorithms.ans.markov_predict_cpp_ext",
                      sourcedir="src/benchcompress/algorithms/ans"),
        CMakeExtension("benchcompress.algorithms.ans.get_run_lengths_cpp_ext",
                      sourcedir="src/benchcompress/algorithms/ans")
    ],
    cmdclass={
        "build_ext": CMakeBuild,
    },
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "benchcompress=benchcompress.cli:main",
        ],
    },
    author="Jeremy Magland",
    description="Benchmarking compression methods for numeric arrays",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="compression, signal processing",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
)
