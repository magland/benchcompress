import numpy as np
import os


SOURCE_FILE = "gaussian/__init__.py"


def _load_long_description():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(current_dir, "gaussian.md")
    with open(md_path, "r", encoding="utf-8") as f:
        return f.read()


LONG_DESCRIPTION = _load_long_description()


def create_gaussian_quantized(
    *, n_samples: int, stddev: float, seed: int
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = np.round(rng.normal(0, stddev, n_samples)).astype(np.int16)
    return x


def create_gaussian_float(*, n_samples: int, stddev: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = rng.normal(0, stddev, n_samples).astype(np.float32)
    return x


tags_quantized = [
    "gaussian",
    "integer",
    "discrete",
    "timeseries",
    "1d",
    "synthetic",
    "i.i.d.",
]
tags_float = ["gaussian", "float", "timeseries", "1d", "synthetic", "i.i.d."]

datasets = [
    {
        "name": "gaussian-q1",
        "version": "1",
        "create": lambda: create_gaussian_quantized(
            n_samples=1_000_000, stddev=1, seed=0
        ),
        "description": "Rounded Gaussian integers with σ=1.",
        "tags": tags_quantized,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "gaussian-q2",
        "version": "1",
        "create": lambda: create_gaussian_quantized(
            n_samples=1_000_000, stddev=2, seed=0
        ),
        "description": "Rounded Gaussian integers with σ=2.",
        "tags": tags_quantized,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "gaussian-q3",
        "version": "1",
        "create": lambda: create_gaussian_quantized(
            n_samples=1_000_000, stddev=3, seed=0
        ),
        "description": "Rounded Gaussian integers with σ=3.",
        "tags": tags_quantized,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "gaussian-q5",
        "version": "1",
        "create": lambda: create_gaussian_quantized(
            n_samples=1_000_000, stddev=5, seed=0
        ),
        "description": "Rounded Gaussian integers with σ=5.",
        "tags": tags_quantized,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "gaussian-q8",
        "version": "1",
        "create": lambda: create_gaussian_quantized(
            n_samples=1_000_000, stddev=8, seed=0
        ),
        "description": "Rounded Gaussian integers with σ=8.",
        "tags": tags_quantized,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "gaussian-flt1",
        "version": "1",
        "create": lambda: create_gaussian_float(n_samples=1_000_000, stddev=8, seed=0),
        "description": "Floating point Gaussian numbers with σ=1.",
        "tags": tags_float,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
]
