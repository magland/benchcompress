# %%
import numpy as np
from zia_benchmark._filters import bandpass_filter, highpass_filter
from zia_benchmark._compress_ints_lossless import compress_ints_lossless
from zia_benchmark.datasets import datasets
# %%
import numpy as np

# %%
import numpy as np
from zia_benchmark._filters import bandpass_filter, highpass_filter
from zia_benchmark._data_loaders import load_real_000876, load_real_000409, load_real_001290
from zia_benchmark._compress_ints_lossless import compress_ints_lossless
from zia_benchmark._analysis import linear_fit, compute_entropy_per_sample, estimate_noise_level
import matplotlib.pyplot as plt

# %%
# Find the real-000409-ch101 dataset
real_dataset = next(d for d in datasets if d['name'] == 'real-000409-ch101')
X = real_dataset['create']().flatten()

X = X.astype(np.int16)

# %%
plt.figure(figsize=(12, 4))
plt.plot(X[:2400])
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
X_filt = bandpass_filter(X - np.median(X), sampling_frequency=30000, lowcut=lowcut, highcut=highcut)
noise_level = estimate_noise_level(X_filt, sampling_frequency=30000)
X_filt_normalized = X_filt / noise_level
X2b = X_filt_normalized / v
X2 = np.round(X2b).astype(np.int16)

# %%
plt.figure(figsize=(12, 4))
plt.plot(X[:2400])

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
plt.plot(X[:2400])
plt.title('RAW')

plt.figure(figsize=(12, 4))
plt.plot(X2[:2400])
plt.title('FILTERED')

plt.figure(figsize=(12, 4))
plt.plot(residuals2[:2400])
plt.title('FILTERED MARCOVIAN')

# %%
def sliding_max(x, delta):
    y = np.zeros_like(x)
    for i in range(len(x)):
        y[i] = np.max(x[max(0, i - delta):min(len(x), i + delta + 1)])
    return y

def smoothed(x, delta):
    y = np.zeros_like(x)
    for i in range(len(x)):
        y[i] = np.mean(x[max(0, i - delta):min(len(x), i + delta + 1)])
    return y

cc = [3, 6]
Y = sliding_max(np.abs(X_filt_normalized), 50)
Y = smoothed(Y, 20)
Y = np.minimum(1, np.maximum(0, (Y - cc[0]) / (cc[1] - cc[0])))
# Y = highpass_filter(Y, sampling_frequency=30000, lowcut=3)
Y_scaled = X_filt_normalized * Y
X3b = Y_scaled / v
X3 = np.round(X3b).astype(np.int16)

plt.figure(figsize=(12, 4))
plt.plot(X2[:2400], color='lightgray')
# plt.plot(Y[4000:5000])
plt.plot(X3b[:2400])
# %%
print('FILTERED (and quantized) with suppression')
print_ideal_compression_ratio(X3)
print('')
print('FILTERED DELTA ENCODING with suppression')
print_ideal_compression_ratio(np.diff(X3))
print('')
print('FILTERED MARCOVIAN with suppression')
residuals3 = get_marcovian_prediction_residual(X3, 20)
print_ideal_compression_ratio(residuals3)
print('ACTUAL FILTERED MARCOVIAN with suppression')
print_actual_compression_ratios(residuals3)
# %%
def get_run_lengths(x):
    runs = []
    i = 0
    current_nonzero_run_length = 0
    while i < len(x):
        if np.all(x[i:i+10] == 0):
            runs.append(current_nonzero_run_length)
            current_nonzero_run_length = 0
            j = i
            while j < len(x) and x[j] == 0:
                j += 1
            runs.append(j - i)
            i = j
        else:
            current_nonzero_run_length += 1
            i += 1
    if np.max(runs) < 256:
        return np.array(runs, dtype=np.uint8)
    if np.max(runs) < 2 ** 16:
        return np.array(runs, dtype=np.uint16)
    return np.array(runs, dtype=np.uint32)

AA = residuals3[residuals3 != 0]
run_lengths = get_run_lengths(residuals3)
print(run_lengths, run_lengths.itemsize)
ee = compute_entropy_per_sample(AA)
theoretical_size = (len(AA) * ee / 8) + run_lengths.nbytes
theoretical_compression_ratio = len(residuals3) * X.itemsize / theoretical_size
print(f'Theoretical compression ratio: {theoretical_compression_ratio:.2f}')
