# Brotli Algorithm

Brotli is a general-purpose data compression algorithm developed by Google. It uses a combination of modern compression techniques including LZ77, Huffman coding, and context modeling.

## Variants

We provide several variants with different compression levels:

### Standard Compression
- brotli-4: Fast compression with moderate ratio
- brotli-6: Balanced between speed and compression
- brotli-8: Better compression at cost of speed
- brotli-11: Maximum compression level

### Delta-Encoded Compression
- brotli-11-delta: Maximum compression with delta encoding

Delta encoding stores differences between consecutive values rather than the values themselves. This can improve compression for sequences where adjacent values are often similar, like time series data.
