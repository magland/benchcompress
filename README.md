# benchcompress

A benchmarking framework for evaluating compression algorithms on numeric timeseries datasets, with a focus on scientific data.

Latest benchmark results: https://magland.github.io/benchcompress/

## Overview

Benchcompress is a comprehensive benchmarking framework for evaluating compression algorithms on numeric timeseries datasets. The system follows an automated workflow:

1. **Defining Components**
   - Algorithms are implemented in `benchcompress/src/benchcompress/algorithms/`
   - Datasets are defined in `benchcompress/src/benchcompress/datasets/`
   - Each component specifies metadata like version, tags, and compatibility requirements

2. **Automated Benchmarking**
   - Benchmarks run automatically via GitHub Actions on pushes to main branch
   - For each compatible algorithm-dataset pair, measures:
     - Compression ratio
     - Encoding throughput (MB/s)
     - Decoding throughput (MB/s)
   - Results are verified by decompressing and comparing with original data

3. **Result Storage**
   - Results are committed to a dedicated `benchmark-results` branch
   - Local and remote caching system prevents redundant rerunning of benchmarks (only modified or added components are re-benchmarked)
   - Caching is based on algorithm and dataset versions

4. **Web Interface**
   - Interactive visualization at https://magland.github.io/benchcompress/
   - Filter and sort results by dataset or algorithm
   - Visual charts for comparing performance metrics
   - Export results to CSV for further analysis

## For developers

The project consists of two main components:

- `benchcompress/`: Python package containing the core benchmarking framework, algorithms, and datasets
- `web-ui/`: React-based web interface for visualizing benchmark results

### Local Development Setup

1. Install Python dependencies:
```bash
cd benchcompress
pip install -e .

benchcompress --help
benchcompress list
benchcompress run --help
```

2. Install web UI dependencies:
```bash
cd web-ui
npm install
```

3. Run web UI locally:
```bash
cd web-ui
npm run dev
```

### Code Formatting

This project uses pre-commit hooks to automatically format code before each commit. The formatting includes:
- Python code formatting using black
- TypeScript/JavaScript code formatting using npm scripts

To set up the pre-commit hooks after cloning the repository:

1. Install pre-commit:
```bash
pip install pre-commit
```

2. Install the git hook scripts:
```bash
pre-commit install
```

After this setup, code will be automatically formatted when you make a commit.

# Theory

For independently and identically distributed (i.i.d.) discrete data, where each sample is drawn from a discrete probability distribution (e.g., Bernoulli sampling or quantized Gaussian noise), the theoretical compression ratio is determined by the Shannon entropy formula:
$$
H(X) = -\sum_{i} p(x_i) \log p(x_i).
$$
Here, $p(x_i)$ represents the probability of occurrence of the $i$-th symbol $x_i$ in the discrete distribution.

In practice, achieving this theoretical compression ratio often requires sophisticated encoding techniques. While arithmetic encoding provides one such method, it is challenging to implement and can be computationally inefficient. A more modern and efficient alternative is Asymmetric Numeric Systems (ANS), which closely approaches the theoretical limit and is incorporated into state-of-the-art compressors such as ZStandard. However, these algorithms are primarily optimized for structured data types, such as text, rather than for scientific numerical timeseries data.

In our benchmarks, we evaluate a simple implementation of ANS using a Python package we developed, called \texttt{simple\_ans}. As anticipated, ANS demonstrates superior performance when compressing i.i.d. samples from a discrete distribution. However, its efficiency diminishes when handling more structured data, such as continuous signals (e.g., voltage traces in electrophysiology).

Applying delta encoding partially mitigates this limitation by leveraging the continuity properties of the data through differencing. This preprocessing step enhances ANS performance, though it still falls short of the compression achieved by methods like ZStandard. Additional preprocessing techniques, such as linear Markov predictive modeling (where the residual error after prediction is compressed instead of the original signal), further improve ANS performance. In these scenarios, the residual data is smaller and exhibits reduced correlation, enabling ANS to achieve better compression results relative to other methods.
