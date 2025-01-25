import numpy as np


SOURCE_FILE = "bernoulli/__init__.py"


def create_bernoulli(*, n_samples: int, p: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = rng.binomial(1, p, n_samples).astype(np.uint8)
    return x


datasets = [
    {
        "name": "bernoulli-0.1",
        "version": "3",
        "create": lambda: create_bernoulli(n_samples=1_000_000, p=0.1, seed=0),
        "description": "Binary sequence with 10% probability of ones.",
        "tags": ["binary"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "bernoulli-0.2",
        "version": "3",
        "create": lambda: create_bernoulli(n_samples=1_000_000, p=0.2, seed=0),
        "description": "Binary sequence with 20% probability of ones.",
        "tags": ["binary"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "bernoulli-0.3",
        "version": "3",
        "create": lambda: create_bernoulli(n_samples=1_000_000, p=0.3, seed=0),
        "description": "Binary sequence with 30% probability of ones.",
        "tags": ["binary"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "bernoulli-0.4",
        "version": "3",
        "create": lambda: create_bernoulli(n_samples=1_000_000, p=0.4, seed=0),
        "description": "Binary sequence with 40% probability of ones.",
        "tags": ["binary"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "bernoulli-0.5",
        "version": "3",
        "create": lambda: create_bernoulli(n_samples=1_000_000, p=0.5, seed=0),
        "description": "Binary sequence with 50% probability of ones and 50% probability of zeros.",
        "tags": ["binary"],
        "source_file": SOURCE_FILE,
    },
]
