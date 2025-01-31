# Bzip2 Algorithm

Bzip2 is a compression algorithm that uses the Burrows-Wheeler transform along with Huffman coding. It typically achieves better compression than traditional LZ77/LZ78-based algorithms but at the cost of speed.

## Variants

### Standard Compression
Different compression levels trading off speed vs compression ratio:
- bzip2-1: Fastest compression
- bzip2-3: Better compression than level 1
- bzip2-5: Medium compression
- bzip2-7: Better compression than level 5
- bzip2-9: Maximum compression

### Delta Encoding
- bzip2-9-delta: Maximum compression with delta encoding

Delta encoding stores differences between consecutive values rather than the values themselves. This can improve compression for sequences where adjacent values are often similar, such as time series data.
