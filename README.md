# zia

A benchmarking framework for evaluating compression algorithms on integer array datasets, with a focus on scientific data.

## Overview

Zia provides systematic benchmarking of compression methods for integer arrays, measuring:
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

## Results

Latest benchmark results: https://magland.github.io/zia/
