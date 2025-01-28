import numpy as np
from .markov_predict_cpp_ext import markov_predict_cpp


def markov_predict(x: np.ndarray, M: int, num_training_samples: int = 10000) -> tuple:
    """Predict signal using Markov model and return coefficients, initial values and residuals using C++ implementation.

    Args:
        x: Input signal (will be converted to int16)
        M: Number of previous samples to use for prediction
        num_training_samples: Maximum number of samples to use for fitting the model coefficients (default: 10000).
                            Using fewer samples speeds up model fitting on large inputs while maintaining accuracy.

    Returns:
        tuple: (coefficients (float32), initial_values (int16), residuals (int16))
    """
    # Call C++ implementation with proper type conversion
    return markov_predict_cpp(x.astype(np.int16), M, num_training_samples)
