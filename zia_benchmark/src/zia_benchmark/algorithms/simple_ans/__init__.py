import numpy as np


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
    header = [
        dtype_code,
        encoded.num_bits,
        encoded.signal_length,
        encoded.state,
        len(encoded.symbol_counts)
    ] + [c for c in encoded.symbol_counts] + [v for v in encoded.symbol_values]
    header_bytes = np.array(header, dtype=np.int64).tobytes()
    header_size = np.uint32(len(header_bytes))
    return header_size.tobytes() + header_bytes + encoded.bitstream


def simple_ans_decode(x: bytes, dtype: str) -> np.ndarray:
    from simple_ans import ans_decode, EncodedSignal
    header_size = np.frombuffer(x[:4], dtype=np.uint32)[0]
    header = np.frombuffer(x[4:4 + header_size], dtype=np.int64)
    dtype_code, num_bits, signal_length, state, num_symbols = header[:5]
    symbol_counts = header[5:5 + num_symbols]
    symbol_values = header[5 + num_symbols:]
    bitstream = x[4 + header_size:]
    if dtype_code == 0:
        assert dtype == 'uint8'
    elif dtype_code == 1:
        assert dtype == 'uint16'
    elif dtype_code == 2:
        assert dtype == 'uint32'
    elif dtype_code == 3:
        assert dtype == 'int16'
    elif dtype_code == 4:
        assert dtype == 'int32'
    else:
        raise ValueError(f"Unsupported dtype code: {dtype_code}")

    encoded = EncodedSignal(
        num_bits=int(num_bits),
        signal_length=int(signal_length),
        state=int(state),
        symbol_counts=symbol_counts.astype(np.uint32),
        symbol_values=symbol_values.astype(dtype),
        bitstream=bitstream
    )
    return ans_decode(encoded)

algorithms = [
    {
        'name': 'simple-ans',
        'version': '1',
        'encode': lambda x: simple_ans_encode(x),
        'decode': lambda x, dtype: simple_ans_decode(x, dtype)
    }
]
