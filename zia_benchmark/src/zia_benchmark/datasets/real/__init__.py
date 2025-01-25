import numpy as np
import lindi
from typing import cast
from ..._filters import bandpass_filter
from ..._analysis import estimate_noise_level


SOURCE_FILE = "real/__init__.py"


def _load_real_000876(
    *, num_samples: int, num_channels: int, start_channel: int
) -> np.ndarray:
    """Load data from DANDI dataset 000876.

    Args:
        num_samples: Number of samples to load
        num_channels: Number of channels to load
        start_channel: Starting channel index

    Returns:
        Array of shape (num_samples, num_channels) containing the loaded data
    """
    nwb_url = "https://api.dandiarchive.org/api/assets/7e1de06d-d478-40e2-9b64-9dd04eafaa4c/download/"
    h5f = lindi.LindiH5pyFile.from_hdf5_file(nwb_url)
    ds = h5f["/acquisition/ElectricalSeriesAP/data"]
    assert isinstance(ds, lindi.LindiH5pyDataset)
    ret = ds[:num_samples, start_channel : start_channel + num_channels]
    return cast(np.ndarray, ret)


def _load_real_000409(
    *, num_samples: int, num_channels: int, start_channel: int
) -> np.ndarray:
    """Load data from DANDI dataset 000409.

    Args:
        num_samples: Number of samples to load
        num_channels: Number of channels to load
        start_channel: Starting channel index

    Returns:
        Array of shape (num_samples, num_channels) containing the loaded data
    """
    nwb_url = "https://api.dandiarchive.org/api/assets/c04f6b30-82bf-40e1-9210-34f0bcd8be24/download/"
    h5f = lindi.LindiH5pyFile.from_hdf5_file(nwb_url)
    ds = h5f["/acquisition/ElectricalSeriesAp/data"]
    assert isinstance(ds, lindi.LindiH5pyDataset)
    ret = ds[:num_samples, start_channel : start_channel + num_channels]
    return cast(np.ndarray, ret)


def _load_real_001290(
    *, num_samples: int, num_channels: int, start_channel: int
) -> np.ndarray:
    """Load data from DANDI dataset 001290.

    Args:
        num_samples: Number of samples to load
        num_channels: Number of channels to load
        start_channel: Starting channel index

    Returns:
        Array of shape (num_samples, num_channels) containing the loaded data
    """
    nwb_url = "https://api.dandiarchive.org/api/assets/78c99d23-da88-4ecd-9086-c488a126eac5/download/"
    h5f = lindi.LindiH5pyFile.from_hdf5_file(nwb_url)
    ds = h5f["/acquisition/ElectricalSeriesAPImec/data"]
    assert isinstance(ds, lindi.LindiH5pyDataset)
    ret = ds[:num_samples, start_channel : start_channel + num_channels]
    return cast(np.ndarray, ret)


def _create_filtered_version(X: np.ndarray) -> np.ndarray:
    """Create filtered version of a dataset using bandpass filtering and quantization.

    Args:
        X: Input signal array

    Returns:
        Filtered and quantized signal array
    """
    v = 0.25  # step size for quantization
    lowcut = 300
    highcut = 6000
    sampling_frequency = 30000

    # Bandpass filter
    X_filt = bandpass_filter(
        X - np.median(X),
        sampling_frequency=sampling_frequency,
        lowcut=lowcut,
        highcut=highcut,
    )

    # Normalize by noise level
    noise_level = estimate_noise_level(X_filt, sampling_frequency=sampling_frequency)
    X_filt_normalized = X_filt / noise_level

    # Quantize
    X2b = X_filt_normalized / v
    X2 = np.round(X2b).astype(np.int16)

    return X2


datasets = [
    {
        "name": "real-000876-ch45",
        "version": "1",
        "description": "Raw extracellular electrophysiology recording from DANDI:000876.",
        "create": lambda: _load_real_000876(
            num_samples=500_000, num_channels=1, start_channel=45
        ).flatten(),
        "tags": ["continuous", "neurophysiology"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "real-000409-ch101",
        "version": "1",
        "description": "Raw extracellular electrophysiology recording from DANDI:000409.",
        "create": lambda: _load_real_000409(
            num_samples=500_000, num_channels=1, start_channel=101
        ).flatten(),
        "tags": ["continuous", "neurophysiology"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "real-001290-ch0",
        "version": "1",
        "description": "Raw extracellular electrophysiology recording from DANDI:001290.",
        "create": lambda: _load_real_001290(
            num_samples=500_000, num_channels=1, start_channel=0
        ).flatten(),
        "tags": ["continuous", "neurophysiology"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "real-000876-ch45-filtered",
        "version": "1",
        "description": "Preprocessed version of real-000876-ch45. Bandpass filtered (300-6000 Hz).",
        "create": lambda: _create_filtered_version(
            _load_real_000876(
                num_samples=500_000, num_channels=1, start_channel=45
            ).flatten()
        ),
        "tags": ["continuous", "neurophysiology", "filtered"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "real-000409-ch101-filtered",
        "version": "1",
        "description": "Preprocessed version of real-000409-ch101. Bandpass filtered (300-6000 Hz).",
        "create": lambda: _create_filtered_version(
            _load_real_000409(
                num_samples=500_000, num_channels=1, start_channel=101
            ).flatten()
        ),
        "tags": ["continuous", "neurophysiology", "filtered"],
        "source_file": SOURCE_FILE,
    },
    {
        "name": "real-001290-ch0-filtered",
        "version": "1",
        "description": "Preprocessed version of real-001290-ch0. Bandpass filtered (300-6000 Hz).",
        "create": lambda: _create_filtered_version(
            _load_real_001290(
                num_samples=500_000, num_channels=1, start_channel=0
            ).flatten()
        ),
        "tags": ["continuous", "neurophysiology", "filtered"],
        "source_file": SOURCE_FILE,
    },
]
