import numpy as np


SOURCE_FILE = "lzma/__init__.py"


def lzma_delta_encode(x: np.ndarray, preset: int) -> bytes:
    import lzma

    assert x.ndim == 1
    y = np.diff(x)
    y = np.insert(y, 0, x[0])
    buf = y.tobytes()
    compressed = lzma.compress(buf, preset=preset)
    return compressed


def lzma_delta_decode(x: bytes, dtype: str) -> np.ndarray:
    import lzma

    buf = lzma.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return np.cumsum(y)


def lzma_encode(x: np.ndarray, preset: int) -> bytes:
    import lzma

    assert x.ndim == 1
    buf = x.tobytes()
    compressed = lzma.compress(buf, preset=preset)
    return compressed


def lzma_decode(x: bytes, dtype: str) -> np.ndarray:
    import lzma

    buf = lzma.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return y


algorithms = [
    {
        "name": "lzma-9",
        "version": "1",
        "encode": lambda x: lzma_encode(x, preset=9),
        "decode": lambda x, dtype: lzma_decode(x, dtype),
        "description": "LZMA compression at maximum preset 9 for highest compression ratio.",
        "source_file": SOURCE_FILE,
    },
    {
        "name": "lzma-9-delta",
        "version": "1",
        "encode": lambda x: lzma_delta_encode(x, preset=9),
        "decode": lambda x, dtype: lzma_delta_decode(x, dtype),
        "description": "LZMA compression at preset 9 with delta encoding for improved compression of sequential data.",
        "tags": ["delta_encoding"],
        "source_file": SOURCE_FILE,
    },
]
