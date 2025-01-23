# %%
import numpy as np
from helpers import bandpass_filter, estimate_noise_level, compute_entropy_per_sample
from load_real import load_real_000876, load_real_000409, load_real_001290
from compress_ints_lossless import compress_ints_lossless

def linear_fit(x, y):
    """Perform linear fit with constant term.
    Returns coefficients and prediction function."""
    from numpy.linalg import lstsq
    X = np.column_stack([x, np.ones(len(x))])
    coeffs = lstsq(X, y, rcond=None)[0]

    def predict(x_new):
        X_new = np.column_stack([x_new, np.ones(len(x_new))])
        return np.dot(X_new, coeffs)

    return coeffs, predict

# %%
N = 500_000
# X = np.round(np.random.randn(N) * 500)

# X = load_real_001290(num_samples=N, num_channels=1, start_channel=0)
X = load_real_000409(num_samples=N, num_channels=1, start_channel=101)
# X = load_real_000876(num_samples=N, num_channels=1, start_channel=45)
# X = np.random.randn(len(X)) * 100

X = X.astype(np.int16)
X = X.flatten()
# %%
e1 = compute_entropy_per_sample(X)
print(f'(raw) Bits per sample: {e1:.2f}')
print(f'Ideal compression ratio: {X.itemsize * 8 / e1:.2f}')

# %%
e1 = compute_entropy_per_sample(np.diff(X))
print(f'(raw diff) Bits per sample: {e1:.2f}')
print(f'Ideal compression ratio: {X.itemsize * 8 / e1:.2f}')

# %%
# Actual compression ratio
buf_zstd = compress_ints_lossless(np.diff(X), method='zstd')
buf_zlib = compress_ints_lossless(np.diff(X), method='zlib')
buf_lzma = compress_ints_lossless(np.diff(X), method='lzma')
buf_ans = compress_ints_lossless(np.diff(X), method='simple_ans')
print(f'Zstd compression ratio: {len(X) * X.itemsize / len(buf_zstd):.2f}')
print(f'Zlib compression ratio: {len(X) * X.itemsize / len(buf_zlib):.2f}')
print(f'Lzma compression ratio: {len(X) * X.itemsize / len(buf_lzma):.2f}')
print(f'Simple ANS compression ratio: {len(X) * X.itemsize / len(buf_ans):.2f}')

# %%
M = 20
# N - M + 1 x M
sequences = np.array([X[i:i+M] for i in range(len(X) - 2 * M + 1)])
predictors = sequences[:, :M - 1]
target = sequences[:, M - 1]

# Can choose either linear or quadratic fit
# coeffs, predict = quadratic_fit(predictors, y)
coeffs, predict = linear_fit(predictors, target)
predictions = predict(predictors)
predictions = np.round(predictions)
residuals = target - predictions
residuals = residuals.astype(np.int16)
e3 = compute_entropy_per_sample(residuals)
print(f'(raw adjusted) Bits per sample: {e3:.2f}')
print(f'Ideal compression ratio: {X.itemsize * 8 / e3:.2f}')

# %%
v = 5
lowcut = 300
highcut = 6000
X2 = bandpass_filter(X - np.median(X), sampling_frequency=30000, lowcut=lowcut, highcut=highcut)
noise_level = estimate_noise_level(X2, sampling_frequency=30000)
X2b = X2 / noise_level * v
X2 = np.round(X2b).astype(np.int16)
e2 = compute_entropy_per_sample(X2)
print(f'(filtered) Bits per sample: {e2:.2f}')
print(f'Ideal compression ratio: {X.itemsize * 8 / e2:.2f}')

# %%
e2 = compute_entropy_per_sample(np.diff(X2))
print(f'(filtered diff) Bits per sample: {e2:.2f}')
print(f'Ideal compression ratio: {X.itemsize * 8 / e2:.2f}')

# %%
M = 20
# N - M + 1 x M
sequences = np.array([X2[i:i+M] for i in range(len(X) - 2 * M + 1)])
predictors = sequences[:, :M - 1]
target = sequences[:, M - 1]

coeffs, predict = linear_fit(predictors, target)
predictions = predict(predictors)
predictions = np.round(predictions)
residuals = target - predictions
residuals = residuals.astype(np.int16)
e3 = compute_entropy_per_sample(residuals)
print(f'(filtered adjusted) Bits per sample: {e3:.2f}')
print(f'Ideal compression ratio: {X.itemsize * 8 / e3:.2f}')
# %%
# Get the actual compression ratio
buf_zstd = compress_ints_lossless(residuals, method='zstd')
buf_zlib = compress_ints_lossless(residuals, method='zlib')
buf_lzma = compress_ints_lossless(residuals, method='lzma')
buf_ans = compress_ints_lossless(residuals, method='simple_ans')
print(f'Zstd compression ratio: {len(residuals) * residuals.itemsize / len(buf_zstd):.2f}')
print(f'Zlib compression ratio: {len(residuals) * residuals.itemsize / len(buf_zlib):.2f}')
print(f'Lzma compression ratio: {len(residuals) * residuals.itemsize / len(buf_lzma):.2f}')
print(f'Simple ANS compression ratio: {len(residuals) * residuals.itemsize / len(buf_ans):.2f}')

# %%
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(X2[:600])
# %%
plt.plot(coeffs)
# %%
