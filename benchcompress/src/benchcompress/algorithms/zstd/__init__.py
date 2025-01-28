import numpy as np
from ..simple_ans.markov_reconstruct import markov_reconstruct as markov_reconstruct_cpp
from ..simple_ans.markov_predict import markov_predict as markov_predict_cpp


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


def zstd_markov_encode(x: np.ndarray, level: int) -> bytes:
    import zstandard as zstd
    import struct

    assert x.ndim == 1
    coeffs, initial, resid = markov_predict_cpp(x, M=6, num_training_samples=10000)

    # Convert coeffs and initial to bytes
    coeffs_bytes = coeffs.tobytes()
    initial_bytes = initial.tobytes()

    # Create header with lengths
    header = struct.pack("QQ", len(coeffs_bytes), len(initial_bytes))

    # Compress residuals
    resid_bytes = resid.tobytes()
    compressor = zstd.ZstdCompressor(level=level)
    compressed_resid = compressor.compress(resid_bytes)

    # Combine all parts
    return header + coeffs_bytes + initial_bytes + compressed_resid


def zstd_markov_decode(x: bytes, dtype: str) -> np.ndarray:
    import zstandard as zstd
    import struct

    # Extract header
    header_size = struct.calcsize("QQ")
    coeffs_len, initial_len = struct.unpack("QQ", x[:header_size])

    # Extract coefficients and initial values
    pos = header_size
    coeffs = np.frombuffer(x[pos : pos + coeffs_len], dtype=np.float32)
    pos += coeffs_len
    initial = np.frombuffer(x[pos : pos + initial_len], dtype=dtype)
    pos += initial_len

    # Decompress residuals
    decompressor = zstd.ZstdDecompressor()
    resid_buf = decompressor.decompress(x[pos:])
    resid = np.frombuffer(resid_buf, dtype=dtype)

    # Reconstruct signal
    output = markov_reconstruct_cpp(coeffs, initial, resid)
    return output


algorithms = [
    {
        "name": "zstd-4",
        "version": "1",
        "encode": lambda x: zstd_encode(x, level=4),
        "decode": lambda x, dtype: zstd_decode(x, dtype),
        "description": "Zstandard compression at level 4 (fast compression).",
        "tags": ["zstd"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zstd-7",
        "version": "1",
        "encode": lambda x: zstd_encode(x, level=7),
        "decode": lambda x, dtype: zstd_decode(x, dtype),
        "description": "Zstandard compression at level 7 (balanced speed/compression).",
        "tags": ["zstd"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zstd-10",
        "version": "1",
        "encode": lambda x: zstd_encode(x, level=10),
        "decode": lambda x, dtype: zstd_decode(x, dtype),
        "description": "Zstandard compression at level 10 (better compression).",
        "tags": ["zstd"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zstd-13",
        "version": "1",
        "encode": lambda x: zstd_encode(x, level=13),
        "decode": lambda x, dtype: zstd_decode(x, dtype),
        "description": "Zstandard compression at level 13 (high compression).",
        "tags": ["zstd"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zstd-16",
        "version": "1",
        "encode": lambda x: zstd_encode(x, level=16),
        "decode": lambda x, dtype: zstd_decode(x, dtype),
        "description": "Zstandard compression at level 16 (very high compression).",
        "tags": ["zstd"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zstd-19",
        "version": "1",
        "encode": lambda x: zstd_encode(x, level=19),
        "decode": lambda x, dtype: zstd_decode(x, dtype),
        "description": "Zstandard compression at level 19 (ultra high compression).",
        "tags": ["zstd"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zstd-22",
        "version": "1",
        "encode": lambda x: zstd_encode(x, level=22),
        "decode": lambda x, dtype: zstd_decode(x, dtype),
        "description": "Zstandard compression at maximum level 22 (highest compression).",
        "tags": ["zstd"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zstd-22-delta",
        "version": "1",
        "encode": lambda x: zstd_delta_encode(x, level=22),
        "decode": lambda x, dtype: zstd_delta_decode(x, dtype),
        "description": "Zstandard compression at level 22 with delta encoding for improved compression of sequential data.",
        "tags": ["zstd", "delta_encoding"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "zstd-22-markov",
        "version": "1",
        "encode": lambda x: zstd_markov_encode(x, level=22),
        "decode": lambda x, dtype: zstd_markov_decode(x, dtype),
        "description": "Zstandard compression at level 22 with Markov prediction for exploiting temporal correlations in the data.",
        "tags": ["zstd", "markov_prediction"],
        "source_file": SOURCE_FILE,
    },
]
