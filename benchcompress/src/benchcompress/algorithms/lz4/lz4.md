# LZ4 Algorithm

LZ4 is a lossless compression algorithm focused on compression and decompression speed. It belongs to the LZ77 family of byte-oriented compression schemes and is particularly well-suited for real-time compression scenarios.

## Variants

### Standard Compression
Different compression levels trading off speed vs compression ratio:
- lz4-0: Fastest compression mode
- lz4-3: Minimum high compression mode
- lz4-10: Higher compression
- lz4-16: Maximum compression

### Delta Encoding
- lz4-16-delta: Maximum compression with delta encoding

Delta encoding stores differences between consecutive values rather than the values themselves. This can improve compression for sequences where adjacent values are often similar, such as time series data.
