import numpy as np
from .markov_reconstruct_cpp_ext import markov_reconstruct_cpp


def markov_reconstruct(coeffs, initial, resid):
    """Reconstruct signal from Markov model parameters and residuals using C++ implementation.

    Args:
        coeffs: Model coefficients from linear regression (float32)
        initial: Initial values needed for prediction (int16)
        resid: Prediction residuals (int16)

    Returns:
        np.ndarray: Reconstructed signal (int16)
    """
    # Call C++ implementation
    return markov_reconstruct_cpp(
        coeffs.astype(np.float32), initial.astype(np.int16), resid.astype(np.int16)
    )
