from .bernoulli import datasets as bernoulli_datasets
from .gaussian import datasets as gaussian_datasets
from .ecephys import datasets as ecephys_datasets
from .seismic import datasets as seismic_datasets
from .ieeg import datasets as ieeg_datasets
from .fmri import datasets as fmri_datasets

datasets_list = [
    bernoulli_datasets,
    gaussian_datasets,
    ecephys_datasets,
    seismic_datasets,
    ieeg_datasets,
    fmri_datasets,
]

datasets = []
for d in datasets_list:
    datasets.extend(d)
