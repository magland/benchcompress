import numpy as np


SOURCE_FILE = "lz4/__init__.py"


def lz4_encode(x: np.ndarray, level: int) -> bytes:
    import lz4.frame

    buf = x.tobytes()
    compressed = lz4.frame.compress(buf, compression_level=level)
    return compressed


def lz4_decode(x: bytes, dtype: str, shape: tuple) -> np.ndarray:
    import lz4.frame

    buf = lz4.frame.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return y.reshape(shape)


def lz4_delta_encode(x: np.ndarray, level: int) -> bytes:
    import lz4.frame

    assert x.ndim == 1
    y = np.diff(x)
    y = np.insert(y, 0, x[0])
    buf = y.tobytes()
    compressed = lz4.frame.compress(buf, compression_level=level)
    return compressed


def lz4_delta_decode(x: bytes, dtype: str, shape: tuple) -> np.ndarray:
    import lz4.frame

    assert len(shape) == 1

    buf = lz4.frame.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return np.cumsum(y)


algorithms = [
    {
        "name": "lz4-0",
        "version": "1",
        "encode": lambda x: lz4_encode(x, level=0),
        "decode": lambda x, dtype, shape: lz4_decode(x, dtype, shape),
        "description": "LZ4 compression at level 0 (fastest).",
        "tags": ["lz4"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "lz4-3",
        "version": "1",
        "encode": lambda x: lz4_encode(x, level=3),
        "decode": lambda x, dtype, shape: lz4_decode(x, dtype, shape),
        "description": "LZ4 compression at level 3 (minimum high compression).",
        "tags": ["lz4"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "lz4-10",
        "version": "1",
        "encode": lambda x: lz4_encode(x, level=10),
        "decode": lambda x, dtype, shape: lz4_decode(x, dtype, shape),
        "description": "LZ4 compression at level 10.",
        "tags": ["lz4"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "lz4-16",
        "version": "1",
        "encode": lambda x: lz4_encode(x, level=16),
        "decode": lambda x, dtype, shape: lz4_decode(x, dtype, shape),
        "description": "LZ4 compression at level 16 (highest compression).",
        "tags": ["lz4"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "lz4-16-delta",
        "version": "1",
        "encode": lambda x: lz4_delta_encode(x, level=16),
        "decode": lambda x, dtype, shape: lz4_delta_decode(x, dtype, shape),
        "description": "LZ4 compression at level 16 with delta encoding.",
        "tags": ["lz4", "delta_encoding", "1d"],
        "source_file": SOURCE_FILE,
    },
]
