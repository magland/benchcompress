import numpy as np


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

algorithms = [
    {
        'name': 'zstd-4',
        'version': '1',
        'encode': lambda x: zstd_encode(x, level=4),
        'decode': lambda x, dtype: zstd_decode(x, dtype)
    },
    {
        'name': 'zstd-7',
        'version': '1',
        'encode': lambda x: zstd_encode(x, level=7),
        'decode': lambda x, dtype: zstd_decode(x, dtype)
    },
    {
        'name': 'zstd-10',
        'version': '1',
        'encode': lambda x: zstd_encode(x, level=10),
        'decode': lambda x, dtype: zstd_decode(x, dtype)
    },
    {
        'name': 'zstd-13',
        'version': '1',
        'encode': lambda x: zstd_encode(x, level=13),
        'decode': lambda x, dtype: zstd_decode(x, dtype)
    },
    {
        'name': 'zstd-16',
        'version': '1',
        'encode': lambda x: zstd_encode(x, level=16),
        'decode': lambda x, dtype: zstd_decode(x, dtype)
    },
    {
        'name': 'zstd-19',
        'version': '1',
        'encode': lambda x: zstd_encode(x, level=19),
        'decode': lambda x, dtype: zstd_decode(x, dtype)
    },
    {
        'name': 'zstd-22',
        'version': '1',
        'encode': lambda x: zstd_encode(x, level=22),
        'decode': lambda x, dtype: zstd_decode(x, dtype)
    }
]
