import numpy as np


def create_gaussian(*, n_samples: int, stddev: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = np.round(rng.normal(0, stddev, n_samples)).astype(np.int16)
    return x

datasets = [
    {
        'name': 'gaussian-1',
        'version': '1',
        'create': lambda: create_gaussian(n_samples=1_000_000, stddev=1, seed=0)
    },
    {
        'name': 'gaussian-2',
        'version': '1',
        'create': lambda: create_gaussian(n_samples=1_000_000, stddev=2, seed=0)
    },
    {
        'name': 'gaussian-3',
        'version': '1',
        'create': lambda: create_gaussian(n_samples=1_000_000, stddev=3, seed=0)
    },
    {
        'name': 'gaussian-5',
        'version': '1',
        'create': lambda: create_gaussian(n_samples=1_000_000, stddev=5, seed=0)
    },
    {
        'name': 'gaussian-8',
        'version': '1',
        'create': lambda: create_gaussian(n_samples=1_000_000, stddev=8, seed=0)
    }
]
