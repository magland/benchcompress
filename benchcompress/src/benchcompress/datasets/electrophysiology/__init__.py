import numpy as np
import lindi
import os
from typing import cast
from ..._filters import bandpass_filter
from ..._analysis import estimate_noise_level


SOURCE_FILE = "electrophysiology/__init__.py"


def _load_long_description():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(current_dir, "electrophysiology.md")
    with open(md_path, "r", encoding="utf-8") as f:
        return f.read()


LONG_DESCRIPTION = _load_long_description()

tags = ["real", "electrophysiology", "timeseries", "1d", "integer", "continuous"]


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


def _load_real_001259(*, num_samples: int) -> np.ndarray:
    """Load data from DANDI dataset 001259.

    Args:
        num_samples: Number of samples to load

    Returns:
        Array of shape (num_samples, 1) containing the loaded data
    """
    # this one only has one channel
    # https://neurosift.app/?p=/nwb&url=https://api.dandiarchive.org/api/assets/6fa78218-f4d4-45f3-a627-5afe4aa88c3e/download/&dandisetId=001259&dandisetVersion=draft
    nwb_url = "https://api.dandiarchive.org/api/assets/6fa78218-f4d4-45f3-a627-5afe4aa88c3e/download/"
    h5f = lindi.LindiH5pyFile.from_hdf5_file(nwb_url)
    ds = h5f["/acquisition/ElectricalSeries"]
    assert isinstance(ds, lindi.LindiH5pyDataset)
    # this one only has one channel
    ret = ds[:num_samples, 0]
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


def _create_sparse_version(X: np.ndarray) -> np.ndarray:
    """Create sparse version of a dataset using activity-based suppression.

    Args:
        X: Input signal array

    Returns:
        Sparse signal array with suppressed low-activity regions
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

    # Activity detection
    def sliding_max(x: np.ndarray, delta: int) -> np.ndarray:
        y = np.zeros_like(x)
        for i in range(len(x)):
            y[i] = np.max(x[max(0, i - delta) : min(len(x), i + delta + 1)])
        return y

    def smoothed(x: np.ndarray, delta: int) -> np.ndarray:
        y = np.zeros_like(x)
        for i in range(len(x)):
            y[i] = np.mean(x[max(0, i - delta) : min(len(x), i + delta + 1)])
        return y

    # Activity detection parameters
    activity_threshold = [3, 6]  # [min, max] thresholds for activity detection

    # Detect activity regions
    Y = sliding_max(np.abs(X_filt_normalized), 50)
    Y = smoothed(Y, 20)
    Y = np.minimum(
        1,
        np.maximum(
            0,
            (Y - activity_threshold[0])
            / (activity_threshold[1] - activity_threshold[0]),
        ),
    )

    # Apply suppression
    Y_scaled = X_filt_normalized * Y
    X3b = Y_scaled / v
    X3 = np.round(X3b).astype(np.int16)

    return X3


datasets = [
    {
        "name": "ephys-000876-ch45",
        "version": "1",
        "description": "Raw extracellular electrophysiology recording from DANDI:000876.",
        "create": lambda: _load_real_000876(
            num_samples=500_000, num_channels=1, start_channel=45
        ).flatten(),
        "tags": tags,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "ephys-000409-ch101",
        "version": "1",
        "description": "Raw extracellular electrophysiology recording from DANDI:000409.",
        "create": lambda: _load_real_000409(
            num_samples=500_000, num_channels=1, start_channel=101
        ).flatten(),
        "tags": tags,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "ephys-001290-ch0",
        "version": "1",
        "description": "Raw extracellular electrophysiology recording from DANDI:001290.",
        "create": lambda: _load_real_001290(
            num_samples=500_000, num_channels=1, start_channel=0
        ).flatten(),
        "tags": tags,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "ephys-001259",
        "version": "1",
        "description": "Raw extracellular electrophysiology recording from DANDI:001259.",
        "create": lambda: _load_real_001259(num_samples=500_000).flatten(),
        "tags": tags,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "ephys-000876-ch45-filtered",
        "version": "1",
        "description": "Preprocessed version of real-000876-ch45. Bandpass filtered (300-6000 Hz).",
        "create": lambda: _create_filtered_version(
            _load_real_000876(
                num_samples=500_000, num_channels=1, start_channel=45
            ).flatten()
        ),
        "tags": tags + ["filtered"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "ephys-000409-ch101-filtered",
        "version": "1",
        "description": "Preprocessed version of real-000409-ch101. Bandpass filtered (300-6000 Hz).",
        "create": lambda: _create_filtered_version(
            _load_real_000409(
                num_samples=500_000, num_channels=1, start_channel=101
            ).flatten()
        ),
        "tags": tags + ["filtered"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "ephys-001290-ch0-filtered",
        "version": "1",
        "description": "Preprocessed version of real-001290-ch0. Bandpass filtered (300-6000 Hz).",
        "create": lambda: _create_filtered_version(
            _load_real_001290(
                num_samples=500_000, num_channels=1, start_channel=0
            ).flatten()
        ),
        "tags": tags + ["filtered"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "ephys-001259-filtered",
        "version": "1",
        "description": "Preprocessed version of real-001259. Bandpass filtered (300-6000 Hz).",
        "create": lambda: _create_filtered_version(
            _load_real_001259(num_samples=500_000).flatten()
        ),
        "tags": tags + ["filtered"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "ephys-000876-ch45-sparse",
        "version": "1",
        "description": "Sparse version of real-000876-ch45. Activity-based suppression applied.",
        "create": lambda: _create_sparse_version(
            _load_real_000876(
                num_samples=500_000, num_channels=1, start_channel=45
            ).flatten()
        ),
        "tags": tags + ["filtered", "sparse"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "ephys-000409-ch101-sparse",
        "version": "1",
        "description": "Sparse version of real-000409-ch101. Activity-based suppression applied.",
        "create": lambda: _create_sparse_version(
            _load_real_000409(
                num_samples=500_000, num_channels=1, start_channel=101
            ).flatten()
        ),
        "tags": tags + ["filtered", "sparse"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "ephys-001290-ch0-sparse",
        "version": "1",
        "description": "Sparse version of real-001290-ch0. Activity-based suppression applied.",
        "create": lambda: _create_sparse_version(
            _load_real_001290(
                num_samples=500_000, num_channels=1, start_channel=0
            ).flatten()
        ),
        "tags": tags + ["filtered", "sparse"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
    {
        "name": "ephys-001259-sparse",
        "version": "1",
        "description": "Sparse version of real-001259. Activity-based suppression applied.",
        "create": lambda: _create_sparse_version(
            _load_real_001259(num_samples=500_000).flatten()
        ),
        "tags": tags + ["filtered", "sparse"],
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    },
]
