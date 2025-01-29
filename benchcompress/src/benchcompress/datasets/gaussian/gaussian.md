# Gaussian Dataset

These datasets contain sequences of numbers drawn from Gaussian distributions with μ=0 and various values of σ. All values are independently and identically distributed (i.i.d.).

## Variants

We provide two types of Gaussian datasets:

### Quantized Integer Variants
Numbers are drawn from a Gaussian distribution then rounded to the nearest integer:
- gaussian-q1 (σ=1)
- gaussian-q2 (σ=2)
- gaussian-q3 (σ=3)
- gaussian-q5 (σ=5)
- gaussian-q8 (σ=8)

The quantization creates discrete integer values, with larger σ values producing a wider spread of integers.

### Floating Point Variant
- gaussian-flt1 (σ=1)

This variant preserves the continuous nature of the Gaussian distribution using 32-bit floating point numbers.
