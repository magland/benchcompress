import numpy as np
from .get_run_lengths_cpp_ext import get_run_lengths_cpp


def get_run_lengths(x: np.ndarray) -> np.ndarray:
    """Calculate run lengths of zeros and non-zeros in a signal using C++ implementation.

    Args:
        x: Input signal (will be converted to int16)

    Returns:
        np.ndarray: Array of run lengths alternating between non-zero and zero runs.
                   The dtype will be uint8, uint16, or uint32 depending on the maximum run length.
    """
    # Call C++ implementation with proper type conversion
    return get_run_lengths_cpp(x.astype(np.int16))
