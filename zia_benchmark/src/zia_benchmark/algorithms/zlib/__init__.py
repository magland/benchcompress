import numpy as np


def zlib_encode(x: np.ndarray, level: int) -> bytes:
    import zlib

    assert x.ndim == 1
    buf = x.tobytes()
    compressed = zlib.compress(buf, level=level)
    return compressed


def zlib_decode(x: bytes, dtype: str) -> np.ndarray:
    import zlib

    buf = zlib.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return y


def zlib_delta_encode(x: np.ndarray, level: int) -> bytes:
    import zlib

    assert x.ndim == 1
    y = np.diff(x)
    y = np.insert(y, 0, x[0])
    buf = y.tobytes()
    compressed = zlib.compress(buf, level=level)
    return compressed


def zlib_delta_decode(x: bytes, dtype: str) -> np.ndarray:
    import zlib

    buf = zlib.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return np.cumsum(y)


algorithms = [
    {
        "name": "zlib-1",
        "version": "1",
        "encode": lambda x: zlib_encode(x, level=1),
        "decode": lambda x, dtype: zlib_decode(x, dtype),
        "tags": [],
    },
    {
        "name": "zlib-3",
        "version": "1",
        "encode": lambda x: zlib_encode(x, level=3),
        "decode": lambda x, dtype: zlib_decode(x, dtype),
        "tags": [],
    },
    {
        "name": "zlib-5",
        "version": "1",
        "encode": lambda x: zlib_encode(x, level=5),
        "decode": lambda x, dtype: zlib_decode(x, dtype),
        "tags": [],
    },
    {
        "name": "zlib-7",
        "version": "1",
        "encode": lambda x: zlib_encode(x, level=7),
        "decode": lambda x, dtype: zlib_decode(x, dtype),
        "tags": [],
    },
    {
        "name": "zlib-9",
        "version": "1",
        "encode": lambda x: zlib_encode(x, level=9),
        "decode": lambda x, dtype: zlib_decode(x, dtype),
        "tags": [],
    },
    {
        "name": "zlib-9-delta",
        "version": "1",
        "encode": lambda x: zlib_delta_encode(x, level=9),
        "decode": lambda x, dtype: zlib_delta_decode(x, dtype),
        "tags": ["delta_encoding"],
    },
]
