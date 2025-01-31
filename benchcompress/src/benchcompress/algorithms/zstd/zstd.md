# Zstandard Algorithm

Zstandard (zstd) is a fast real-time compression algorithm developed by Facebook. It provides a wide range of compression levels and supports custom dictionaries for improved compression.

## Variants

### Standard Compression
Different compression levels trading off speed vs compression ratio:
- zstd-4: Fast compression
- zstd-7: Balanced speed/compression
- zstd-10: Better compression
- zstd-13: High compression
- zstd-16: Very high compression
- zstd-19: Ultra high compression
- zstd-22: Maximum compression

### Advanced Variants

#### Delta Encoding (zstd-22-delta)
Stores differences between consecutive values. Effective for sequences where adjacent values are similar, like time series data.

#### Markov Prediction (zstd-22-markov)
Uses a Markov model to predict values based on previous samples. The prediction residuals are then compressed using zstd. This can significantly improve compression for data with temporal correlations.

#### Markov with Zero RLE (zstd-22-markov-zrle)
Combines Markov prediction with zero run-length encoding. Particularly effective for sparse data where many values are zero, as it efficiently encodes runs of zeros while using Markov prediction for the non-zero regions.
