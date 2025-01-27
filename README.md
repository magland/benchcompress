# zia

A benchmarking framework for evaluating compression algorithms on numeric array datasets, with a focus on scientific data.

## Overview

Zia provides systematic benchmarking of compression methods for numeric arrays, measuring:
- Compression ratio
- Encoding throughput (MB/s)
- Decoding throughput (MB/s)

## Repository Structure

Key components are located in the `zia_benchmark/src/zia_benchmark/` directory:

- Algorithms: `/algorithms/`
  - LZMA: `/algorithms/lzma/`
  - Zstandard: `/algorithms/zstd/`
  - ZLIB: `/algorithms/zlib/`
  - Simple ANS: `/algorithms/simple_ans/`
  - etc.

- Datasets: `/datasets/`
  - Synthetic data generators:
    - `/datasets/bernoulli/`: Binary random data
    - `/datasets/gaussian/`: Normal distribution samples
  - Real data: `/datasets/real/`
  - etc.

- Core functionality:
  - `run_benchmarks.py`: Main benchmarking engine

## Development

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

## Results

Latest benchmark results: https://magland.github.io/zia/
