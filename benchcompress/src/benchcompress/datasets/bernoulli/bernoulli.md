# Bernoulli Dataset

A Bernoulli dataset is a sequence of binary values (0s and 1s) where each value is independently generated with a fixed probability `p` of being 1. These datasets are useful for testing compression algorithms because they have well-defined theoretical properties.

## Variants

We provide five variants with different probabilities of generating a 1:
- bernoulli-0.1 (10% ones)
- bernoulli-0.2 (20% ones)
- bernoulli-0.3 (30% ones)
- bernoulli-0.4 (40% ones)
- bernoulli-0.5 (50% ones)

## Theoretical Properties

The theoretical entropy H(p) provides a lower bound for compression:
```
H(p) = -p log₂(p) - (1-p) log₂(1-p) bits/symbol
```

For example, at p = 0.1 the theoretical minimum is 0.469 bits/symbol, while at p = 0.5 it reaches the maximum of 1.000 bits/symbol.
