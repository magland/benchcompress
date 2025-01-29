# LZMA Algorithm

LZMA (Lempel-Ziv-Markov chain Algorithm) is a compression algorithm that provides high compression ratios. It uses a dictionary compression scheme similar to LZ77 but with sophisticated modeling of repeating patterns using Markov chains.

## Variants

### Standard Compression
- lzma-9: Maximum compression preset (level 9)
  - Focuses on achieving the highest possible compression ratio
  - Uses larger dictionary sizes and more complex modeling
  - Generally slower than other compression algorithms but produces smaller files

### Delta Encoding
- lzma-9-delta: Maximum compression with delta encoding

Delta encoding stores differences between consecutive values rather than the values themselves. This can improve compression for sequences where adjacent values are often similar, such as time series data.
