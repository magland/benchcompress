# Zlib Algorithm

Zlib is a data compression library that uses the DEFLATE algorithm, which combines LZ77 and Huffman coding. It provides a good balance between compression ratio and speed, making it widely used in many applications.

## Variants

### Standard Compression
Different compression levels trading off speed vs compression ratio:
- zlib-1: Fastest compression
- zlib-3: Better compression than level 1
- zlib-5: Medium compression
- zlib-7: Better compression than level 5
- zlib-9: Maximum compression

### Delta Encoding
- zlib-9-delta: Maximum compression with delta encoding

Delta encoding stores differences between consecutive values rather than the values themselves. This can improve compression for sequences where adjacent values are often similar, such as time series data.
