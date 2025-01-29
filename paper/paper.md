# Benchmarking Compression Algorithms for Scientific Data Arrays

*Jeremy Magland, Center for Computational Mathematics, Flatiron Institute*

*Last updated: January 2025*

**This is a draft paper, work in progress.**

## Abstract

*Benchcompress* is a benchmarking framework designed to evaluate the performance of various compression algorithms on scientific data arrays. The framework automates the benchmarking process, measuring compression ratio, encoding throughput, and decoding throughput for each algorithm-dataset pair. Results are verified through decompression and comparison with the original data, ensuring accuracy and reliability. The benchmark results are stored and visualized through an interactive web interface, allowing users to filter, sort, and explore the data. This paper presents the design, implementation, and preliminary results of Benchcompress, highlighting its utility in identifying optimal compression techniques for scientific datasets.

## Introduction

[To be added]

## Theory

For independently and identically distributed (i.i.d.) discrete data, where each sample is drawn from a discrete probability distribution (e.g., Bernoulli sampling or quantized Gaussian noise), the theoretical compressed size in bits per sample is determined by the Shannon entropy formula:

$$
H(X) = -\sum_{i} p(x_i) \log_2 p(x_i).
$$

Here, $p(x_i)$ represents the probability of occurrence of the $i$-th symbol $x_i$ in the discrete distribution. So for example, if we have a Bernoulli distribution with $p=0.5$, the entropy is

$$
H_{\text{Bernoulli, p=0.5}} = -0.5 \log_2 0.5 - 0.5 \log_2 0.5 = 1
$$

bits per sample. This means that the optimal compression ratio for such a dataset is 8, assuming the samples are stored as 8-bit integers. On the other hand, if $p\neq 0.5$, the entropy becomes lower and we can achieve compression at a rate of less than 1 bit per sample (e.g., for $p=0.1$, the entropy is around 0.47 bits per sample, so the compression ratio would be around 17).

In practice, achieving this theoretical compression ratio requires sophisticated encoding techniques. Arithmetic encoding [ref] is one such method, but it is challenging to implement and can be computationally inefficient. A more modern and efficient alternative is Asymmetric Numeric Systems (ANS) [ref], which closely approaches the theoretical limit and is incorporated into state-of-the-art compressors such as ZStandard [ref]. However, these algorithms are primarily optimized for structured data types, such as text, rather than for numeric scientific data.

In our benchmarks, we evaluate a simple implementation of ANS using a Python package called `simple_ans`. As anticipated, ANS demonstrates superior performance when compressing i.i.d. samples from a discrete distribution. However, its efficiency diminishes when handling more structured data, such as continuous signals (e.g., voltage traces in electrophysiology).

Applying delta encoding partially mitigates this limitation by leveraging the continuity properties of the data through differencing. This preprocessing step enhances ANS performance, though it still falls short of the compression achieved by methods like ZStandard. Additional preprocessing techniques, such as linear Markov predictive modeling, further improve ANS performance by exploiting temporal correlations in the data.

The Markov prediction scheme employs a linear autoregressive model where each sample is predicted as a linear combination of $M$ previous samples. For a given integer time series $x[t]$, the prediction $\hat{x}[t]$ is computed as:

$$
\hat{x}[t] = \text{round}\left(\sum_{i=1}^M c_i x[t-i] + b\right)
$$

where the coefficients $c_i$ and bias term $b$ are determined through least squares regression on a subset of the data. The rounding operation ensures integer predictions. Rather than compressing the original signal directly, the algorithm compresses the integer residual error sequence $r[t] = x[t] - \hat{x}[t]$. This approach proves effective because the residuals typically have smaller magnitude compared with the original signal or with the deltas. The compression process stores three components: the floating-point model coefficients, a small set of initial integer values required to begin prediction, and the compressed integer residual sequence. During reconstruction, the original signal is recovered by computing predictions and adding back the residuals:

$$
x[t] = \text{round}\left(\sum_{i=1}^M c_i x[t-i] + b\right) + r[t]
$$

This predictive preprocessing step improves compression performance compared to applying ANS (or other algorithms) directly to either the raw signal or delta-encoded data.

## Methods

### Compression Algorithms

Describe the various compression methods.

### Dataset Generation

Describe the datasets we use for benchmarking.

## Implementation

[To be added]

## Results

[Preliminary results to be added]

## Discussion

[Discussion to be added]

## Conclusion

[Conclusion to be added]
