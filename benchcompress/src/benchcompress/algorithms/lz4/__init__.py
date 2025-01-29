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
        "name": "lz4-1",
        "version": "1",
        "encode": lambda x: lz4_encode(x, level=1),
        "decode": lambda x, dtype, shape: lz4_decode(x, dtype, shape),
        "description": "LZ4 compression at level 1 (fastest).",
        "tags": ["lz4"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "lz4-3",
        "version": "1",
        "encode": lambda x: lz4_encode(x, level=3),
        "decode": lambda x, dtype, shape: lz4_decode(x, dtype, shape),
        "description": "LZ4 compression at level 3.",
        "tags": ["lz4"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "lz4-6",
        "version": "1",
        "encode": lambda x: lz4_encode(x, level=6),
        "decode": lambda x, dtype, shape: lz4_decode(x, dtype, shape),
        "description": "LZ4 compression at level 6.",
        "tags": ["lz4"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "lz4-9",
        "version": "1",
        "encode": lambda x: lz4_encode(x, level=9),
        "decode": lambda x, dtype, shape: lz4_decode(x, dtype, shape),
        "description": "LZ4 compression at level 9.",
        "tags": ["lz4"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "lz4-12",
        "version": "1",
        "encode": lambda x: lz4_encode(x, level=12),
        "decode": lambda x, dtype, shape: lz4_decode(x, dtype, shape),
        "description": "LZ4 compression at maximum level 12.",
        "tags": ["lz4"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "lz4-12-delta",
        "version": "1",
        "encode": lambda x: lz4_delta_encode(x, level=12),
        "decode": lambda x, dtype, shape: lz4_delta_decode(x, dtype, shape),
        "description": "LZ4 compression at level 12 with delta encoding.",
        "tags": ["lz4", "delta_encoding", "1d"],
        "source_file": SOURCE_FILE,
    },
]
