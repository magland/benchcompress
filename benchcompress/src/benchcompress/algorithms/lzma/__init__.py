import numpy as np
import os


SOURCE_FILE = "lzma/__init__.py"


def _load_long_description():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(current_dir, "lzma.md")
    with open(md_path, "r", encoding="utf-8") as f:
        return f.read()


LONG_DESCRIPTION = _load_long_description()


def lzma_delta_encode(x: np.ndarray, preset: int) -> bytes:
    import lzma

    assert x.ndim == 1
    y = np.diff(x)
    y = np.insert(y, 0, x[0])
    buf = y.tobytes()
    compressed = lzma.compress(buf, preset=preset)
    return compressed


def lzma_delta_decode(x: bytes, dtype: str, shape: tuple) -> np.ndarray:
    import lzma

    assert len(shape) == 1

    buf = lzma.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return np.cumsum(y)


def lzma_encode(x: np.ndarray, preset: int) -> bytes:
    import lzma

    buf = x.tobytes()
    compressed = lzma.compress(buf, preset=preset)
    return compressed


def lzma_decode(x: bytes, dtype: str, shape: tuple) -> np.ndarray:
    import lzma

    buf = lzma.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return y.reshape(shape)


algorithms = [
    {
        "name": "lzma-9",
        "version": "1",
        "encode": lambda x: lzma_encode(x, preset=9),
        "decode": lambda x, dtype, shape: lzma_decode(x, dtype, shape),
        "description": "LZMA compression at maximum preset 9 for highest compression ratio.",
        "tags": ["lzma"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "lzma-9-delta",
        "version": "1",
        "encode": lambda x: lzma_delta_encode(x, preset=9),
        "decode": lambda x, dtype, shape: lzma_delta_decode(x, dtype, shape),
        "description": "LZMA compression at preset 9 with delta encoding for improved compression of sequential data.",
        "tags": ["lzma", "delta_encoding", "1d"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
]
