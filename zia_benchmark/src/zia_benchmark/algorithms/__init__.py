from .zlib import algorithms as zlib_algorithms
from .zstd import algorithms as zstd_algorithms
from .simple_ans import algorithms as simple_ans_algorithms
from .lzma import algorithms as lzma_algorithms

algorithms = zlib_algorithms + zstd_algorithms + simple_ans_algorithms + lzma_algorithms
