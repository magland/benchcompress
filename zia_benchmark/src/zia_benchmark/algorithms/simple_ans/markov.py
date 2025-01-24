import numpy as np
from zia_benchmark._analysis import linear_fit


def markov_predict(x: np.ndarray, M: int) -> tuple:
    """Predict signal using Markov model and return coefficients, initial values and residuals.

    Args:
        x: Input signal
        M: Number of previous samples to use for prediction (default: 20)

    Returns:
        tuple: (coefficients, initial_values, residuals)
    """
    # Keep initial values for reconstruction
    initial = x[: M - 1]

    # Create sequences of M consecutive samples
    sequences = np.array([x[i : i + M] for i in range(len(x) - M + 1)])
    predictors = sequences[:, : M - 1]  # Use M-1 previous samples to predict
    target = sequences[:, M - 1]  # The value to predict

    # Get coefficients and prediction function using linear regression
    coeffs, predict = linear_fit(predictors, target)

    # Make predictions using the linear model
    predictions = predict(predictors)
    predictions = np.round(predictions)

    # Calculate residuals (difference between actual and predicted values)
    residuals = target - predictions
    residuals = residuals.astype(x.dtype)

    return coeffs, initial, residuals


def markov_reconstruct(
    coeffs: np.ndarray, initial: np.ndarray, resid: np.ndarray
) -> np.ndarray:
    """Reconstruct signal from Markov model parameters and residuals.

    Args:
        coeffs: Model coefficients from linear regression
        initial: Initial values needed for prediction
        resid: Prediction residuals

    Returns:
        np.ndarray: Reconstructed signal
    """
    M = len(initial) + 1  # Number of samples used in prediction
    output = np.zeros(len(resid) + len(initial), dtype=resid.dtype)
    output[: len(initial)] = initial  # Set initial values

    # Reconstruct signal iteratively
    for i in range(len(resid)):
        # Get previous M-1 values to make prediction
        prev_values = output[i : i + M - 1]
        # Make prediction using coefficients
        prediction = np.sum(coeffs[1:] * prev_values) + coeffs[0]
        prediction = np.round(prediction)
        # Add residual to get actual value
        output[i + M - 1] = prediction + resid[i]

    return output
