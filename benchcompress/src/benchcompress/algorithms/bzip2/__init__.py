import numpy as np
import os


SOURCE_FILE = "bzip2/__init__.py"


def _load_long_description():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(current_dir, "bzip2.md")
    with open(md_path, "r", encoding="utf-8") as f:
        return f.read()


LONG_DESCRIPTION = _load_long_description()


def bzip2_encode(x: np.ndarray, level: int) -> bytes:
    import bz2

    buf = x.tobytes()
    compressed = bz2.compress(buf, compresslevel=level)
    return compressed


def bzip2_decode(x: bytes, dtype: str, shape: tuple) -> np.ndarray:
    import bz2

    buf = bz2.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return y.reshape(shape)


def bzip2_delta_encode(x: np.ndarray, level: int) -> bytes:
    import bz2

    assert x.ndim == 1
    y = np.diff(x)
    y = np.insert(y, 0, x[0])
    buf = y.tobytes()
    compressed = bz2.compress(buf, compresslevel=level)
    return compressed


def bzip2_delta_decode(x: bytes, dtype: str, shape: tuple) -> np.ndarray:
    import bz2

    assert len(shape) == 1

    buf = bz2.decompress(x)
    y = np.frombuffer(buf, dtype=dtype)
    return np.cumsum(y)


algorithms = [
    {
        "name": "bzip2-1",
        "version": "1",
        "encode": lambda x: bzip2_encode(x, level=1),
        "decode": lambda x, dtype, shape: bzip2_decode(x, dtype, shape),
        "description": "Bzip2 compression at level 1 (fastest).",
        "tags": ["bzip2"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "bzip2-3",
        "version": "1",
        "encode": lambda x: bzip2_encode(x, level=3),
        "decode": lambda x, dtype, shape: bzip2_decode(x, dtype, shape),
        "description": "Bzip2 compression at level 3.",
        "tags": ["bzip2"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "bzip2-5",
        "version": "1",
        "encode": lambda x: bzip2_encode(x, level=5),
        "decode": lambda x, dtype, shape: bzip2_decode(x, dtype, shape),
        "description": "Bzip2 compression at level 5 (medium).",
        "tags": ["bzip2"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "bzip2-7",
        "version": "1",
        "encode": lambda x: bzip2_encode(x, level=7),
        "decode": lambda x, dtype, shape: bzip2_decode(x, dtype, shape),
        "description": "Bzip2 compression at level 7.",
        "tags": ["bzip2"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "bzip2-9",
        "version": "1",
        "encode": lambda x: bzip2_encode(x, level=9),
        "decode": lambda x, dtype, shape: bzip2_decode(x, dtype, shape),
        "description": "Bzip2 compression at maximum level 9.",
        "tags": ["bzip2"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "bzip2-9-delta",
        "version": "1",
        "encode": lambda x: bzip2_delta_encode(x, level=9),
        "decode": lambda x, dtype, shape: bzip2_delta_decode(x, dtype, shape),
        "description": "Bzip2 compression at level 9 with delta encoding.",
        "tags": ["bzip2", "delta_encoding", "1d"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
]
