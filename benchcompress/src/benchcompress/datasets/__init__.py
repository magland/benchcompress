from .bernoulli import datasets as bernoulli_datasets
from .gaussian import datasets as gaussian_datasets
from .real import datasets as real_datasets

datasets = bernoulli_datasets + gaussian_datasets + real_datasets
