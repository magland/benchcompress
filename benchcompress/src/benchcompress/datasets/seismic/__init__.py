import numpy as np
import segyio
import os
import requests


SOURCE_FILE = "seismic/__init__.py"


def _load_long_description():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(current_dir, "seismic.md")
    with open(md_path, "r", encoding="utf-8") as f:
        return f.read()


LONG_DESCRIPTION = _load_long_description()

tags = ["real", "seismic", "continuous", "timeseries", "1d"]
tags_float = tags + ["float"]
tags_integer = tags + ["integer"]


def _load_04A_04B_seismic_data() -> np.ndarray:
    """Load seismic data from the SEG-Y file.

    Returns:
        Array containing the loaded seismic data
    """
    file_path = "04A+04B.segy"
    if not os.path.exists(file_path):
        # Download the SEG-Y file
        url = "https://zenodo.org/records/8152964/files/04A+04B.segy?download=1"
        response = requests.get(url)
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {file_path}")
    else:
        print(f"{file_path} already exists locally.")

    # Open the SEG-Y file
    with segyio.open(file_path, "r", ignore_geometry=True) as f:
        # Read the seismic data
        data = f.trace.raw[:]

    # Consider only the first 3000 traces, because the others have a bunch of zeros
    X = data[:3000]
    # The first part of each trace is zeros
    first_nonzero_indices = []
    for j in range(X.shape[0]):
        inds = np.where(X[j] != 0)[0]
        first_nonzero_indices.append(inds[0] if len(inds) > 0 else -1)
    # plt.figure(figsize=(10, 5))
    # plt.hist(first_nonzero_indices, bins=20)
    # print(np.max(first_nonzero_indices)) # 1607
    X = X[:, 1700:]

    return X.ravel()


def _load_quantized_04A_04B_seismic_data():
    X = _load_04A_04B_seismic_data()
    step = 10
    X = np.round(X / step).astype(np.int32)
    return X


def _load_lim_2024_seismic_data() -> np.ndarray:
    """Load seismic data from the 2022 Goesan earthquake.

    Returns:
        Array containing the loaded seismic data
    """
    file_path = "lim_et_al_2024.01.concat.npy"
    if not os.path.exists(file_path):
        # Download the numpy array file
        url = "https://zenodo.org/records/14774624/files/lim_et_al_2024.01.concat.npy?download=1"
        response = requests.get(url)
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {file_path}")
    else:
        print(f"{file_path} already exists locally.")

    # Load the numpy array
    X = np.load(file_path)
    return X


def _load_quantized_lim_2024_seismic_data():
    X = _load_lim_2024_seismic_data()
    step = 10000
    X = np.round(X / step).astype(np.int32)
    return X


datasets = [
    {
        "name": "seismic-04A-04B",
        "version": "1",
        "description": "Seismic data from Roger Revelle voyage RR1508.",
        "create": lambda: _load_04A_04B_seismic_data(),
        "tags": tags_float,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "seismic-04A-04B-quantized",
        "version": "2",
        "description": "Seismic data from Roger Revelle voyage RR1508, quantized.",
        "create": lambda: _load_quantized_04A_04B_seismic_data(),
        "tags": tags_integer,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "seismic-lim-2024-01",
        "version": "1",
        "description": "Seismic data from the 2022 Mw 3.8 Goesan earthquake in South Korea.",
        "create": lambda: _load_lim_2024_seismic_data(),
        "tags": tags_float,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "seismic-lim-2024-01-quantized",
        "version": "1",
        "description": "Seismic data from the 2022 Mw 3.8 Goesan earthquake in South Korea, quantized.",
        "create": lambda: _load_quantized_lim_2024_seismic_data(),
        "tags": tags_integer,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
]
