import numpy as np
import os
import requests
import pyedflib

SOURCE_FILE = "ieeg/__init__.py"


def _load_long_description():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(current_dir, "ieeg.md")
    with open(md_path, "r", encoding="utf-8") as f:
        return f.read()


LONG_DESCRIPTION = _load_long_description()

tags = ["real", "ecephys", "ieeg", "timeseries", "1d", "float", "continuous"]


def _load_ieeg_openneuro_005592() -> np.ndarray:
    """Load data from OpenNeuro dataset 005592.

    Returns:
        Array containing concatenated data from first 10 channels
    """
    url = "https://s3.amazonaws.com/openneuro.org/ds005592/sub-01/ses-01/ieeg/sub-01_ses-01_task-sws_run-01_ieeg.edf?versionId=Wzkwm2FFGDOkhswsxPeqvZr3m5toyWlj"
    edf_filename = "sub-01_ieeg.edf"

    # Download if needed
    if not os.path.exists(edf_filename):
        print(f"Downloading {edf_filename}...")
        response = requests.get(url)
        with open(edf_filename, "wb") as f:
            f.write(response.content)

    # Load and concatenate channels
    f = pyedflib.EdfReader(edf_filename)
    max_channels = 10
    n_signals = min(f.signals_in_file, max_channels)

    # Read and concatenate first n_signals
    signals = []
    for i in range(n_signals):
        signals.append(f.readSignal(i))
    concatenated = np.concatenate(signals).astype(np.float32)

    f.close()
    return concatenated


datasets = [
    {
        "name": "ieeg-005592",
        "version": "1",
        "description": "iEEG recording from OpenNeuro dataset ds005592, first 10 channels concatenated.",
        "create": lambda: _load_ieeg_openneuro_005592(),
        "tags": tags,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    }
]
