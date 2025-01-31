import numpy as np
from ._filters import highpass_filter


def estimate_noise_level(array: np.ndarray, *, sampling_frequency: float) -> float:
    """Estimate the noise level of a signal using the median absolute deviation.

    Args:
        array: Input signal array
        sampling_frequency: Sampling frequency in Hz

    Returns:
        Estimated noise level
    """
    array_filtered = highpass_filter(
        array, sampling_frequency=sampling_frequency, lowcut=300
    )
    MAD = float(
        np.median(np.abs(array_filtered.ravel() - np.median(array_filtered.ravel())))
        / 0.6745
    )
    return MAD


def compute_entropy_per_sample(array: np.ndarray) -> float:
    """Compute the entropy per sample of a signal.

    Args:
        array: Input signal array

    Returns:
        Entropy per sample in bits
    """
    _, counts = np.unique(array, return_counts=True)
    p = counts / len(array)
    return float(-np.sum(p * np.log2(p)))


from typing import Callable


def linear_fit(
    x: np.ndarray, y: np.ndarray
) -> tuple[np.ndarray, Callable[[np.ndarray], np.ndarray]]:
    """Perform linear fit with constant term.

    Args:
        x: Input array of shape (N, M-1) containing M-1 predictors for N samples
        y: Target array of shape (N,) containing values to predict

    Returns:
        Tuple containing:
        - coefficients array of shape (M,)
        - prediction function that takes x_new and returns predictions
    """
    from numpy.linalg import lstsq

    X = np.column_stack([x, np.ones(len(x))])
    coeffs = lstsq(X, y, rcond=None)[0]

    def predict(x_new: np.ndarray) -> np.ndarray:
        X_new = np.column_stack([x_new, np.ones(len(x_new))])
        return np.dot(X_new, coeffs)

    return coeffs, predict
