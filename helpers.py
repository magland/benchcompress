import numpy as np

def bandpass_filter(array, *, sampling_frequency, lowcut, highcut) -> np.ndarray:
    from scipy.signal import butter, lfilter

    nyquist = 0.5 * sampling_frequency
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(5, [low, high], btype="band")
    return lfilter(b, a, array, axis=0)  # type: ignore

def lowpass_filter(array, *, sampling_frequency, highcut) -> np.ndarray:
    from scipy.signal import butter, lfilter

    nyquist = 0.5 * sampling_frequency
    high = highcut / nyquist
    b, a = butter(5, high, btype="low")
    return lfilter(b, a, array, axis=0)  # type: ignore


def highpass_filter(array, *, sampling_frequency, lowcut) -> np.ndarray:
    from scipy.signal import butter, lfilter

    nyquist = 0.5 * sampling_frequency
    low = lowcut / nyquist
    b, a = butter(5, low, btype="high")
    return lfilter(b, a, array, axis=0)  # type: ignore


def estimate_noise_level(array: np.ndarray, *, sampling_frequency: float) -> float:
    array_filtered = highpass_filter(
        array, sampling_frequency=sampling_frequency, lowcut=300
    )
    MAD = float(
        np.median(np.abs(array_filtered.ravel() - np.median(array_filtered.ravel())))
        / 0.6745
    )
    return MAD


def compute_entropy_per_sample(a):
    _, counts = np.unique(a, return_counts=True)
    p = counts / len(a)
    return -np.sum(p * np.log2(p))
