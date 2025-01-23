def compress_ints_lossless(x, *, method: str = "zstd") -> bytes:
    import zstandard as zstd

    if method == "zstd":
        cctx = zstd.ZstdCompressor(level=22)
        return cctx.compress(x.tobytes())
    elif method == "zlib":
        import zlib
        return zlib.compress(x.tobytes(), level=9)
    elif method == "lzma":
        import lzma
        return lzma.compress(x.tobytes(), preset=9)
    elif method == "simple_ans":
        from simple_ans import ans_encode
        encoding = ans_encode(x)
        return encoding.bitstream + encoding.symbol_counts.tobytes() + encoding.symbol_values.tobytes()
    else:
        raise ValueError(f"Unknown method: {method}")