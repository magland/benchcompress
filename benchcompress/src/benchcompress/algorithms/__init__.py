from .zlib import algorithms as zlib_algorithms
from .zstd import algorithms as zstd_algorithms
from .ans import algorithms as ans_algorithms
from .lzma import algorithms as lzma_algorithms
from .brotli import algorithms as brotli_algorithms

algorithms = (
    zlib_algorithms
    + zstd_algorithms
    + ans_algorithms
    + lzma_algorithms
    + brotli_algorithms
)
