import numpy as np


SOURCE_FILE = "zlib/__init__.py"


def zlib_encode(x: np.ndarray, level: int) -> bytes:
    import zlib

    buf = x.tobytes()
    compressed = zlib.compress(buf, level=level)
    return compressed


def zlib_decode(x: bytes, dtype: str, shape: tuple) -> np.ndarray:
    import zlib

    buf = zlib.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return y.reshape(shape)


def zlib_delta_encode(x: np.ndarray, level: int) -> bytes:
    import zlib

    assert x.ndim == 1
    y = np.diff(x)
    y = np.insert(y, 0, x[0])
    buf = y.tobytes()
    compressed = zlib.compress(buf, level=level)
    return compressed


def zlib_delta_decode(x: bytes, dtype: str, shape: tuple) -> np.ndarray:
    import zlib

    assert len(shape) == 1

    buf = zlib.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return np.cumsum(y)


algorithms = [
    {
        "name": "zlib-1",
        "version": "1",
        "encode": lambda x: zlib_encode(x, level=1),
        "decode": lambda x, dtype, shape: zlib_decode(x, dtype, shape),
        "description": "Zlib DEFLATE compression at level 1 (fastest).",
        "tags": ["zlib"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zlib-3",
        "version": "1",
        "encode": lambda x: zlib_encode(x, level=3),
        "decode": lambda x, dtype, shape: zlib_decode(x, dtype, shape),
        "description": "Zlib DEFLATE compression at level 3.",
        "tags": ["zlib"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zlib-5",
        "version": "1",
        "encode": lambda x: zlib_encode(x, level=5),
        "decode": lambda x, dtype, shape: zlib_decode(x, dtype, shape),
        "description": "Zlib DEFLATE compression at level 5 (medium).",
        "tags": ["zlib"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zlib-7",
        "version": "1",
        "encode": lambda x: zlib_encode(x, level=7),
        "decode": lambda x, dtype, shape: zlib_decode(x, dtype, shape),
        "description": "Zlib DEFLATE compression at level 7.",
        "tags": ["zlib"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zlib-9",
        "version": "1",
        "encode": lambda x: zlib_encode(x, level=9),
        "decode": lambda x, dtype, shape: zlib_decode(x, dtype, shape),
        "description": "Zlib DEFLATE compression at maximum level 9.",
        "tags": ["zlib"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zlib-9-delta",
        "version": "1",
        "encode": lambda x: zlib_delta_encode(x, level=9),
        "decode": lambda x, dtype, shape: zlib_delta_decode(x, dtype, shape),
        "description": "Zlib DEFLATE compression at level 9 with delta encoding.",
        "tags": ["zlib", "delta_encoding", "1d"],
        "source_file": SOURCE_FILE,
    },
]
