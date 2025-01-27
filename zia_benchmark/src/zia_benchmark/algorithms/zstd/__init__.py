import numpy as np


SOURCE_FILE = "zstd/__init__.py"


def zstd_delta_encode(x: np.ndarray, level: int) -> bytes:
    import zstandard as zstd

    assert x.ndim == 1
    y = np.diff(x)
    y = np.insert(y, 0, x[0])
    buf = y.tobytes()
    compressor = zstd.ZstdCompressor(level=level)
    compressed = compressor.compress(buf)
    return compressed


def zstd_delta_decode(x: bytes, dtype: str) -> np.ndarray:
    import zstandard as zstd

    decompressor = zstd.ZstdDecompressor()
    buf = decompressor.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return np.cumsum(y)


def zstd_encode(x: np.ndarray, level: int) -> bytes:
    import zstandard as zstd

    assert x.ndim == 1
    buf = x.tobytes()
    compressor = zstd.ZstdCompressor(level=level)
    compressed = compressor.compress(buf)
    return compressed


def zstd_decode(x: bytes, dtype: str) -> np.ndarray:
    import zstandard as zstd

    decompressor = zstd.ZstdDecompressor()
    buf = decompressor.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return y


algorithms = [
    {
        "name": "zstd-4",
        "version": "1",
        "encode": lambda x: zstd_encode(x, level=4),
        "decode": lambda x, dtype: zstd_decode(x, dtype),
        "description": "Zstandard compression at level 4 (fast compression).",
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zstd-7",
        "version": "1",
        "encode": lambda x: zstd_encode(x, level=7),
        "decode": lambda x, dtype: zstd_decode(x, dtype),
        "description": "Zstandard compression at level 7 (balanced speed/compression).",
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zstd-10",
        "version": "1",
        "encode": lambda x: zstd_encode(x, level=10),
        "decode": lambda x, dtype: zstd_decode(x, dtype),
        "description": "Zstandard compression at level 10 (better compression).",
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zstd-13",
        "version": "1",
        "encode": lambda x: zstd_encode(x, level=13),
        "decode": lambda x, dtype: zstd_decode(x, dtype),
        "description": "Zstandard compression at level 13 (high compression).",
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zstd-16",
        "version": "1",
        "encode": lambda x: zstd_encode(x, level=16),
        "decode": lambda x, dtype: zstd_decode(x, dtype),
        "description": "Zstandard compression at level 16 (very high compression).",
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zstd-19",
        "version": "1",
        "encode": lambda x: zstd_encode(x, level=19),
        "decode": lambda x, dtype: zstd_decode(x, dtype),
        "description": "Zstandard compression at level 19 (ultra high compression).",
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zstd-22",
        "version": "1",
        "encode": lambda x: zstd_encode(x, level=22),
        "decode": lambda x, dtype: zstd_decode(x, dtype),
        "description": "Zstandard compression at maximum level 22 (highest compression).",
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zstd-22-delta",
        "version": "1",
        "encode": lambda x: zstd_delta_encode(x, level=22),
        "decode": lambda x, dtype: zstd_delta_decode(x, dtype),
        "description": "Zstandard compression at level 22 with delta encoding for improved compression of sequential data.",
        "tags": ["delta_encoding"],
        "source_file": SOURCE_FILE,
    },
]
