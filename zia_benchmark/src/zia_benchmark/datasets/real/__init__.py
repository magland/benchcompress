import numpy as np
import lindi
from typing import cast


def _load_real_000876(*, num_samples: int, num_channels: int, start_channel: int) -> np.ndarray:
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
    ret = ds[:num_samples, start_channel:start_channel + num_channels]
    return cast(np.ndarray, ret)


def _load_real_000409(*, num_samples: int, num_channels: int, start_channel: int) -> np.ndarray:
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
    ds = h5f['/acquisition/ElectricalSeriesAp/data']
    assert isinstance(ds, lindi.LindiH5pyDataset)
    ret = ds[:num_samples, start_channel:start_channel + num_channels]
    return cast(np.ndarray, ret)


def _load_real_001290(*, num_samples: int, num_channels: int, start_channel: int) -> np.ndarray:
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
    ds = h5f['/acquisition/ElectricalSeriesAPImec/data']
    assert isinstance(ds, lindi.LindiH5pyDataset)
    ret = ds[:num_samples, start_channel:start_channel + num_channels]
    return cast(np.ndarray, ret)


datasets = [
    {
        'name': 'real-000876-ch45',
        'version': '1',
        'description': 'Real neurophysiology data from DANDI:000876, channel 45',
        'create': lambda: _load_real_000876(num_samples=500_000, num_channels=1, start_channel=45).flatten()
    },
    {
        'name': 'real-000409-ch101',
        'version': '1',
        'description': 'Real neurophysiology data from DANDI:000409, channel 101',
        'create': lambda: _load_real_000409(num_samples=500_000, num_channels=1, start_channel=101).flatten()
    },
    {
        'name': 'real-001290-ch0',
        'version': '1',
        'description': 'Real neurophysiology data from DANDI:001290, channel 0',
        'create': lambda: _load_real_001290(num_samples=500_000, num_channels=1, start_channel=0).flatten()
    }
]
