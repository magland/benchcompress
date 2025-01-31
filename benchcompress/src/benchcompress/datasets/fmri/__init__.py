import numpy as np
import os
import nibabel as nib
from typing import cast, Optional, List

SOURCE_FILE = "fmri/__init__.py"


def _load_long_description():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(current_dir, "fmri.md")
    with open(md_path, "r", encoding="utf-8") as f:
        return f.read()


LONG_DESCRIPTION = _load_long_description()

tags = ["real", "fmri", "timeseries", "1d", "integer", "bold", "continuous"]


def _load_bold_data(*, slice_indices: Optional[List[int]] = None) -> np.ndarray:
    """Load BOLD fMRI data from OpenNeuro dataset ds005880.

    Args:
        slice_indices: Optional list of slice indices to load. If None, loads full volume.
                      Use range(15, 30) for middle 15 slices.

    Returns:
        Array of shape (X, Y, Z, T) where X,Y,Z are spatial dimensions and T is time points.
        Z dimension will be length 1 if a single slice index is provided.
    """
    url = "https://s3.amazonaws.com/openneuro.org/ds005880/sub-01/func/sub-01_task-rest_run-01_bold.nii.gz?versionId=0z5_YvqoLC4pXDVUVDt9Y1nrJBRxMqXb"
    # Download and load the data
    import requests
    from pathlib import Path

    cache_dir = Path(os.path.expanduser("~/.cache/benchcompress/fmri"))
    cache_dir.mkdir(parents=True, exist_ok=True)
    local_file = cache_dir / "sub-01_task-rest_run-01_bold.nii.gz"

    if not local_file.exists():
        response = requests.get(url)
        response.raise_for_status()
        local_file.write_bytes(response.content)

    img = nib.load(str(local_file))  # type: ignore
    data = img.get_fdata()  # type: ignore

    # Convert to int16
    data = data.astype(np.int16)

    if slice_indices is not None:
        data = data[:, :, slice_indices, :]

    # Now we are going to convert to 1d array, and we make sure that the time dimension varies the fastest
    data = data.ravel()

    return data


datasets = [
    {
        "name": "fmri-ds005880",
        "version": "2",
        "description": "Middle 15 slices from BOLD fMRI recording from ds005880 OpenNeuro dataset.",
        "create": lambda: _load_bold_data(slice_indices=list(range(15, 30))),
        "tags": tags,
        "source_file": SOURCE_FILE,
        "long_description": LONG_DESCRIPTION,
    }
]
