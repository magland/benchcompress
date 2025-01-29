import numpy as np
from .markov_reconstruct_cpp_ext import (
    markov_reconstruct_int16,
    markov_reconstruct_int32,
)


def markov_reconstruct(coeffs, initial, resid):
    """Reconstruct signal from Markov model parameters and residuals using C++ implementation.

    Args:
        coeffs: Model coefficients from linear regression (float32)
        initial: Initial values needed for prediction (int16 or int32)
        resid: Prediction residuals (must match initial dtype)

    Returns:
        np.ndarray: Reconstructed signal (same dtype as input)

    Raises:
        ValueError: If initial/resid arrays are not int16 or int32, or if their dtypes don't match
    """
    # Convert coeffs to float32 if needed
    coeffs = coeffs.astype(np.float32)

    # Check input dtypes
    if initial.dtype != resid.dtype:
        raise ValueError(
            f"Initial and residual arrays must have same dtype, got {initial.dtype} and {resid.dtype}"
        )

    # Call appropriate implementation based on dtype
    if initial.dtype == np.int16:
        return markov_reconstruct_int16(coeffs, initial, resid)
    elif initial.dtype == np.int32:
        return markov_reconstruct_int32(coeffs, initial, resid)
    else:
        raise ValueError(
            f"Initial/residual arrays must be int16 or int32, got {initial.dtype}"
        )
