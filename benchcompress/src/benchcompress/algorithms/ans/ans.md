# ANS (Asymmetric Numeral Systems) Algorithm

ANS is a modern entropy coding method that achieves a compression ratio near arithmetic coding with relatively efficient encoding and decoding. It achieves this by maintaining a state that represents the encoded data in a way that can be efficiently updated. The implementation uses the [simple_ans](https://github.com/flatironinstitute/simple_ans) Python package.

## Variants

### Basic ANS
- ANS: Standard implementation using the simple_ans library
- Efficiently encodes integer data by modeling symbol frequencies

### Delta Encoding
- ANS-delta: ANS compression with delta encoding
- Stores differences between consecutive values
- Effective for sequences where adjacent values are similar

### Markov Prediction
- ANS-markov: ANS with Markov prediction
- Uses a 6th-order Markov model to predict values based on previous samples
- Compresses the prediction residuals
- Particularly effective for data with temporal correlations

### Markov with Zero RLE
- ANS-markov-zrle: Combines Markov prediction with zero run-length encoding
- Identifies runs of zero values and encodes their lengths
- Applies Markov prediction to the non-zero regions
- Ideal for sparse data with many zeros interspersed with correlated non-zero values
