import numpy as np
from .markov_predict_cpp_ext import markov_predict_int16, markov_predict_int32


def markov_predict(x: np.ndarray, M: int, num_training_samples: int = 10000) -> tuple:
    """Predict signal using Markov model and return coefficients, initial values and residuals using C++ implementation.

    Args:
        x: Input signal (must be int16 or int32)
        M: Number of previous samples to use for prediction
        num_training_samples: Maximum number of samples to use for fitting the model coefficients (default: 10000).
                            Using fewer samples speeds up model fitting on large inputs while maintaining accuracy.

    Returns:
        tuple: (coefficients (float32), initial_values (same dtype as input), residuals (same dtype as input))

    Raises:
        ValueError: If input array is not int16 or int32
    """
    # Check input dtype and call appropriate implementation
    if x.dtype == np.int16:
        return markov_predict_int16(x, M, num_training_samples)
    elif x.dtype == np.int32:
        return markov_predict_int32(x, M, num_training_samples)
    else:
        raise ValueError(f"Input array must be int16 or int32, got {x.dtype}")
