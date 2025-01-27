import numpy as np
from zia_benchmark.algorithms.simple_ans.markov_reconstruct_wrapper import (
    markov_reconstruct as markov_reconstruct_cpp,
)
from .markov import markov_predict

SOURCE_FILE = "simple_ans/__init__.py"


def simple_ans_encode(x: np.ndarray) -> bytes:
    from simple_ans import ans_encode

    assert x.ndim == 1
    encoded = ans_encode(x)
    if x.dtype == np.uint8:
        dtype_code = 0
    elif x.dtype == np.uint16:
        dtype_code = 1
    elif x.dtype == np.uint32:
        dtype_code = 2
    elif x.dtype == np.int16:
        dtype_code = 3
    elif x.dtype == np.int32:
        dtype_code = 4
    else:
        raise ValueError(f"Unsupported dtype: {x.dtype}")
    header = (
        [
            dtype_code,
            encoded.num_bits,
            encoded.signal_length,
            encoded.state,
            len(encoded.symbol_counts),
        ]
        + [c for c in encoded.symbol_counts]
        + [v for v in encoded.symbol_values]
    )
    header_bytes = np.array(header, dtype=np.int64).tobytes()
    header_size = np.uint32(len(header_bytes))
    return header_size.tobytes() + header_bytes + encoded.bitstream


def simple_ans_decode(x: bytes, dtype: str) -> np.ndarray:
    from simple_ans import ans_decode, EncodedSignal

    header_size = np.frombuffer(x[:4], dtype=np.uint32)[0]
    header = np.frombuffer(x[4 : 4 + header_size], dtype=np.int64)
    dtype_code, num_bits, signal_length, state, num_symbols = header[:5]
    symbol_counts = header[5 : 5 + num_symbols]
    symbol_values = header[5 + num_symbols :]
    bitstream = x[4 + header_size :]
    if dtype_code == 0:
        assert dtype == "uint8"
    elif dtype_code == 1:
        assert dtype == "uint16"
    elif dtype_code == 2:
        assert dtype == "uint32"
    elif dtype_code == 3:
        assert dtype == "int16"
    elif dtype_code == 4:
        assert dtype == "int32"
    else:
        raise ValueError(f"Unsupported dtype code: {dtype_code}")

    encoded = EncodedSignal(
        num_bits=int(num_bits),
        signal_length=int(signal_length),
        state=int(state),
        symbol_counts=symbol_counts.astype(np.uint32),
        symbol_values=symbol_values.astype(dtype),
        bitstream=bitstream,
    )
    return ans_decode(encoded)


def simple_ans_delta_encode(x: np.ndarray) -> bytes:
    from simple_ans import ans_encode

    assert x.ndim == 1
    y = np.diff(x)
    # Encode just the differences
    encoded = ans_encode(y)
    if x.dtype == np.uint8:
        dtype_code = 0
    elif x.dtype == np.uint16:
        dtype_code = 1
    elif x.dtype == np.uint32:
        dtype_code = 2
    elif x.dtype == np.int16:
        dtype_code = 3
    elif x.dtype == np.int32:
        dtype_code = 4
    else:
        raise ValueError(f"Unsupported dtype: {x.dtype}")
    # Include x[0] in the header
    header = (
        [
            dtype_code,
            encoded.num_bits,
            encoded.signal_length,
            encoded.state,
            len(encoded.symbol_counts),
            x[0],  # Store first value in header
        ]
        + [c for c in encoded.symbol_counts]
        + [v for v in encoded.symbol_values]
    )
    header_bytes = np.array(header, dtype=np.int64).tobytes()
    header_size = np.uint32(len(header_bytes))
    return header_size.tobytes() + header_bytes + encoded.bitstream


def simple_ans_delta_decode(x: bytes, dtype: str) -> np.ndarray:
    from simple_ans import ans_decode, EncodedSignal

    header_size = np.frombuffer(x[:4], dtype=np.uint32)[0]
    header = np.frombuffer(x[4 : 4 + header_size], dtype=np.int64)
    dtype_code, num_bits, signal_length, state, num_symbols, x0 = header[
        :6
    ]  # Extract x0 from header
    symbol_counts = header[6 : 6 + num_symbols]
    symbol_values = header[6 + num_symbols :]
    bitstream = x[4 + header_size :]
    if dtype_code == 0:
        assert dtype == "uint8"
    elif dtype_code == 1:
        assert dtype == "uint16"
    elif dtype_code == 2:
        assert dtype == "uint32"
    elif dtype_code == 3:
        assert dtype == "int16"
    elif dtype_code == 4:
        assert dtype == "int32"
    else:
        raise ValueError(f"Unsupported dtype code: {dtype_code}")

    encoded = EncodedSignal(
        num_bits=int(num_bits),
        signal_length=int(signal_length),
        state=int(state),
        symbol_counts=symbol_counts.astype(np.uint32),
        symbol_values=symbol_values.astype(dtype),
        bitstream=bitstream,
    )
    # Decode the differences
    diffs = ans_decode(encoded)
    # Insert x0 at the beginning and cumulatively sum the differences
    return np.cumsum(np.insert(diffs, 0, x0))


def simple_ans_markov_encode(x: np.ndarray) -> bytes:
    from simple_ans import ans_encode

    assert x.ndim == 1
    coeffs, initial, resid = markov_predict(x, M=10)
    # Encode just the differences
    encoded = ans_encode(resid)
    if x.dtype == np.uint8:
        dtype_code = 0
    elif x.dtype == np.uint16:
        dtype_code = 1
    elif x.dtype == np.uint32:
        dtype_code = 2
    elif x.dtype == np.int16:
        dtype_code = 3
    elif x.dtype == np.int32:
        dtype_code = 4
    else:
        raise ValueError(f"Unsupported dtype: {x.dtype}")
    # Include x[0] in the header
    header = (
        [
            dtype_code,
            encoded.num_bits,
            encoded.signal_length,
            encoded.state,
            len(encoded.symbol_counts),
            len(coeffs),
            len(initial),
        ]
        + [c for c in encoded.symbol_counts]
        + [v for v in encoded.symbol_values]
        + [c for c in coeffs]
        + [v for v in initial]
    )
    header_bytes = np.array(header, dtype=np.float64).tobytes()
    header_size = np.uint32(len(header_bytes))
    return header_size.tobytes() + header_bytes + encoded.bitstream


def simple_ans_markov_decode(x: bytes, dtype: str) -> np.ndarray:
    from simple_ans import ans_decode, EncodedSignal

    header_size = np.frombuffer(x[:4], dtype=np.uint32)[0]
    header = np.frombuffer(x[4 : 4 + header_size], dtype=np.float64)
    dtype_code, num_bits, signal_length, state, num_symbols, num_coeffs, num_initial = (
        header[:7]
    )
    dtype_code = int(dtype_code)
    num_bits = int(num_bits)
    signal_length = int(signal_length)
    state = int(state)
    num_symbols = int(num_symbols)
    num_coeffs = int(num_coeffs)
    num_initial = int(num_initial)

    pos = 7
    symbol_counts = header[pos : pos + num_symbols]
    pos += num_symbols
    symbol_values = header[pos : pos + num_symbols]
    pos += num_symbols
    coeffs = header[pos : pos + num_coeffs]
    pos += num_coeffs
    initial = header[pos : pos + num_initial]
    pos += num_initial
    bitstream = x[4 + header_size :]
    if dtype_code == 0:
        assert dtype == "uint8"
    elif dtype_code == 1:
        assert dtype == "uint16"
    elif dtype_code == 2:
        assert dtype == "uint32"
    elif dtype_code == 3:
        assert dtype == "int16"
    elif dtype_code == 4:
        assert dtype == "int32"
    else:
        raise ValueError(f"Unsupported dtype code: {dtype_code}")

    encoded = EncodedSignal(
        num_bits=int(num_bits),
        signal_length=int(signal_length),
        state=int(state),
        symbol_counts=symbol_counts.astype(np.uint32),
        symbol_values=symbol_values.astype(dtype),
        bitstream=bitstream,
    )
    import time

    resid = ans_decode(encoded)
    output = markov_reconstruct_cpp(coeffs, initial, resid)
    return output


algorithms = [
    {
        "name": "simple-ans",
        "version": "3",
        "encode": lambda x: simple_ans_encode(x),
        "decode": lambda x, dtype: simple_ans_decode(x, dtype),
        "description": "Basic Asymmetric Numeral Systems (ANS) entropy coding for efficient data compression.",
        "source_file": SOURCE_FILE,
    },
    {
        "name": "simple-ans-delta",
        "version": "3",
        "encode": lambda x: simple_ans_delta_encode(x),
        "decode": lambda x, dtype: simple_ans_delta_decode(x, dtype),
        "description": "ANS compression with delta encoding for improved compression of sequential data.",
        "tags": ["delta_encoding"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "simple-ans-markov",
        "version": "5",
        "encode": lambda x: simple_ans_markov_encode(x),
        "decode": lambda x, dtype: simple_ans_markov_decode(x, dtype),
        "description": "ANS compression with Markov prediction for exploiting temporal correlations in the data.",
        "tags": ["markov_prediction"],
        "source_file": SOURCE_FILE,
    },
]
