# %%
import numpy as np
import matplotlib.pyplot as plt
import os
import requests
import segyio

file_path = "04A+04B.segy"
if not os.path.exists(file_path):
    # Download the SEG-Y file
    url = "https://zenodo.org/records/8152964/files/04A+04B.segy?download=1"
    response = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(response.content)
    print(f"Downloaded {file_path}")
else:
    print(f"{file_path} already exists locally.")

# Open the SEG-Y file
with segyio.open(file_path, "r", ignore_geometry=True) as f:
    # Read the seismic data
    data = f.trace.raw[:]
# %%
print(data.shape)  # (4101, 3751)
print(data.dtype)  # float32
# %%
# Consider only the first 3000 traces, because the others have a bunch of zeros
X = data[:3000]
# The first part of each trace is zeros
first_nonzero_indices = []
for j in range(X.shape[0]):
    inds = np.where(X[j] != 0)[0]
    first_nonzero_indices.append(inds[0] if len(inds) > 0 else -1)
# plt.figure(figsize=(10, 5))
# plt.hist(first_nonzero_indices, bins=20)
print(np.max(first_nonzero_indices))  # 1607
X = X[:, 1700:]
# %%
plt.figure(figsize=(10, 5))
plt.plot(X.ravel()[:12000])
# %%
print(X.shape)  # (4101, 2051)
print(X[0, :5])  # [-2891.2651  -2550.8093  -2744.9373   -111.93254  6441.383  ]
# %%
plt.figure(figsize=(10, 5))
plt.plot(X[0])
plt.figure(figsize=(10, 5))
plt.plot(X[1])
plt.figure(figsize=(10, 5))
plt.plot(X[1000])
plt.figure(figsize=(10, 5))
plt.plot(X[1001])
plt.figure(figsize=(10, 5))
plt.plot(X[2000])
plt.figure(figsize=(10, 5))
plt.plot(X[-1])
# %%
plt.figure(figsize=(10, 5))
plt.plot(X[:, 0])
plt.figure(figsize=(10, 5))
plt.plot(X[:, 1])
plt.figure(figsize=(10, 5))
plt.plot(X[:, 1000])
# %%
# Extract the exponent part of the float32 array X as uint8
X_exponent = ((X.view(np.uint32) >> 23) & 0xFF).astype(np.uint8)
print(X_exponent)

# %%
import simple_ans

a = simple_ans.ans_encode(X_exponent.ravel())
# %%
vals, counts = np.unique(X.ravel(), return_counts=True)
print(len(vals))
print(len(X.ravel()))
# plt.figure(figsize=(10, 5))
# plt.plot(vals, '.')

# %%
v = len(a.bitstream) + a.symbol_counts.nbytes + a.symbol_values.nbytes
compression_ratio = len(X_exponent.tobytes()) / v
print(compression_ratio)

print(4 / (v / X_exponent.size + 3))

steps = np.exp(np.arange(20))
tests = []
for step in steps:
    X_quantized = np.round(X / step).astype(np.int32)
    resid = X / step - X_quantized
    resid_delta = np.diff(np.diff(resid.ravel()))
    v = np.median(np.abs(resid_delta))
    tests.append(v)

plt.figure(figsize=(10, 5))
plt.plot(steps, tests)
plt.semilogx()

# %%
q_step = 10000
X_quantized = np.round(X / q_step).astype(np.int32)

# %%
plt.figure(figsize=(10, 5))
plt.plot(X_quantized[0])
plt.figure(figsize=(10, 5))
plt.plot(X[0])
# %%
import simple_ans

a = simple_ans.ans_encode(X_quantized.ravel())
v = len(a.bitstream) + a.symbol_counts.nbytes + a.symbol_values.nbytes
print(len(X.tobytes()) / v)
# %%
import zstandard as zstd

cctx = zstd.ZstdCompressor(level=13)
compressed = cctx.compress(X_quantized.tobytes())
v_zstd = len(compressed)
print(len(X.tobytes()) / v_zstd)
# %%
X_quantized_diff = np.diff(X_quantized.ravel())
a = simple_ans.ans_encode(X_quantized_diff)
v = len(a.bitstream) + a.symbol_counts.nbytes + a.symbol_values.nbytes
print(len(X.tobytes()) / v)
# %%
compressed = cctx.compress(X_quantized_diff.tobytes())
v_zstd = len(compressed)
print(len(X.tobytes()) / v_zstd)
# %%
