# %%
import numpy as np
from zia._filters import bandpass_filter
from zia._data_loaders import load_real_000876, load_real_000409, load_real_001290
from zia._compress_ints_lossless import compress_ints_lossless
from zia._analysis import linear_fit, compute_entropy_per_sample, estimate_noise_level

# %%
N = 500_000

# X = load_real_001290(num_samples=N, num_channels=1, start_channel=0)
X = load_real_000409(num_samples=N, num_channels=1, start_channel=101)
# X = load_real_000876(num_samples=N, num_channels=1, start_channel=45)

X = X.astype(np.int16)
X = X.flatten()
# %%
def print_ideal_compression_ratio(X):
    ee = compute_entropy_per_sample(X)
    print(f'Ideal compression ratio: {X.itemsize * 8 / ee:.2f} ({ee:.2f} bits per sample)')

def print_actual_compression_ratios(X):
    buf_zstd = compress_ints_lossless(X, method='zstd')
    buf_zlib = compress_ints_lossless(X, method='zlib')
    buf_lzma = compress_ints_lossless(X, method='lzma')
    buf_ans = compress_ints_lossless(X, method='simple_ans')
    print(f'Zstd compression ratio: {len(X) * X.itemsize / len(buf_zstd):.2f}')
    print(f'Zlib compression ratio: {len(X) * X.itemsize / len(buf_zlib):.2f}')
    print(f'Lzma compression ratio: {len(X) * X.itemsize / len(buf_lzma):.2f}')
    print(f'simple_ans compression ratio: {len(X) * X.itemsize / len(buf_ans):.2f}')

def get_marcovian_prediction_residual(X, M):
    sequences = np.array([X[i:i+M] for i in range(len(X) - 2 * M + 1)])
    predictors = sequences[:, :M - 1]
    target = sequences[:, M - 1]

    coeffs, predict = linear_fit(predictors, target)
    predictions = predict(predictors)
    predictions = np.round(predictions)
    residuals = target - predictions
    residuals = residuals.astype(np.int16)
    return residuals

# %%
print('RAW')
print_ideal_compression_ratio(X)

# %%
print('RAW DELTA ENCODING')
print_ideal_compression_ratio(np.diff(X))

# %%
print('RAW DELTA ENCODING - actual compression ratios')
print_actual_compression_ratios(np.diff(X))
print_ideal_compression_ratio(np.diff(X))

# %%
X_mr = get_marcovian_prediction_residual(X, 20)
print('RAW MARCOVIAN')
print_ideal_compression_ratio(X_mr)

# %%
v = 0.25  # step size for quantization
lowcut = 300
highcut = 6000
X2 = bandpass_filter(X - np.median(X), sampling_frequency=30000, lowcut=lowcut, highcut=highcut)
noise_level = estimate_noise_level(X2, sampling_frequency=30000)
X2b = X2 / noise_level / v
X2 = np.round(X2b).astype(np.int16)

# %%
print('FILTERED (and quantized)')
print_ideal_compression_ratio(X2)

# %%
print('FILTERED DELTA ENCODING')
print_ideal_compression_ratio(np.diff(X2))

# %%
residuals2 = get_marcovian_prediction_residual(X2, 20)
print('FILTERED MARCOVIAN')
print_ideal_compression_ratio(residuals2)

# %%
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 4))
plt.plot(X[:800])
plt.title('RAW')

plt.figure(figsize=(12, 4))
plt.plot(X2[:800])
plt.title('FILTERED')

plt.figure(figsize=(12, 4))
plt.plot(residuals2[:800])
plt.title('FILTERED MARCOVIAN')

# %%
