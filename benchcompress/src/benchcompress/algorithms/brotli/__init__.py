import numpy as np
import brotli


SOURCE_FILE = "brotli/__init__.py"


def brotli_delta_encode(x: np.ndarray, level: int) -> bytes:
    assert x.ndim == 1
    y = np.diff(x)
    y = np.insert(y, 0, x[0])
    buf = y.tobytes()
    compressed = brotli.compress(buf, quality=level)
    return compressed


def brotli_delta_decode(x: bytes, dtype: str, shape: tuple) -> np.ndarray:
    assert len(shape) == 1
    buf = brotli.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return np.cumsum(y)


def brotli_encode(x: np.ndarray, level: int) -> bytes:
    buf = x.tobytes()
    compressed = brotli.compress(buf, quality=level)
    return compressed


def brotli_decode(x: bytes, dtype: str, shape: tuple) -> np.ndarray:
    buf = brotli.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return y.reshape(shape)


algorithms = [
    {
        "name": "brotli-4",
        "version": "1",
        "encode": lambda x: brotli_encode(x, level=4),
        "decode": lambda x, dtype, shape: brotli_decode(x, dtype, shape),
        "description": "Brotli compression at level 4 (faster).",
        "tags": ["brotli"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "brotli-6",
        "version": "1",
        "encode": lambda x: brotli_encode(x, level=6),
        "decode": lambda x, dtype, shape: brotli_decode(x, dtype, shape),
        "description": "Brotli compression at level 6 (balanced).",
        "tags": ["brotli"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "brotli-8",
        "version": "1",
        "encode": lambda x: brotli_encode(x, level=8),
        "decode": lambda x, dtype, shape: brotli_decode(x, dtype, shape),
        "description": "Brotli compression at level 8 (better compression).",
        "tags": ["brotli"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "brotli-11",
        "version": "1",
        "encode": lambda x: brotli_encode(x, level=11),
        "decode": lambda x, dtype, shape: brotli_decode(x, dtype, shape),
        "description": "Brotli compression at maximum level 11.",
        "tags": ["brotli"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "brotli-11-delta",
        "version": "1",
        "encode": lambda x: brotli_delta_encode(x, level=11),
        "decode": lambda x, dtype, shape: brotli_delta_decode(x, dtype, shape),
        "description": "Brotli compression at level 11 with delta encoding.",
        "tags": ["brotli", "delta_encoding", "1d"],
        "source_file": SOURCE_FILE,
    },
]
