import numpy as np
from .get_run_lengths_cpp_ext import get_run_lengths_int16, get_run_lengths_int32


def get_run_lengths(x: np.ndarray) -> np.ndarray:
    """Calculate run lengths of zeros and non-zeros in a signal using C++ implementation.

    Args:
        x: Input signal (must be int16 or int32)

    Returns:
        np.ndarray: Array of run lengths alternating between non-zero and zero runs.
                   The dtype will be uint8, uint16, or uint32 depending on the maximum run length.

    Raises:
        ValueError: If input array is not int16 or int32
    """
    # Check input dtype and call appropriate implementation
    if x.dtype == np.int16:
        return get_run_lengths_int16(x)
    elif x.dtype == np.int32:
        return get_run_lengths_int32(x)
    else:
        raise ValueError(f"Input array must be int16 or int32, got {x.dtype}")
