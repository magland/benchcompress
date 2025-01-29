from .bernoulli import datasets as bernoulli_datasets
from .gaussian import datasets as gaussian_datasets
from .electrophysiology import datasets as real_datasets
from .seismic import datasets as seismic_datasets

datasets_list = [bernoulli_datasets, gaussian_datasets, real_datasets, seismic_datasets]

datasets = []
for d in datasets_list:
    datasets.extend(d)
