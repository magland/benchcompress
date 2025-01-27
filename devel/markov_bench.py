import numpy as np
import time
from sklearn.linear_model import LinearRegression

########################################################################
# 1) Functions to build the design matrix in float32
########################################################################

def build_design_matrix_naive(x: np.ndarray, M: int):
    """
    Naive Python approach to build design matrix A for Markov model.
    x is int16, but we'll cast to float32 in A.
    A has shape (N - M, M + 1).
    Row j = [1, x_{j+M-1}, x_{j+M-2}, ..., x_{j+M-M}],
    for j in 0..(N-M-1).
    """
    N = len(x)
    A = np.ones((N - M, M + 1), dtype=np.float32)  # store as float32
    for row_idx in range(N - M):
        for k in range(1, M + 1):
            # cast x (int16) to float32 on assignment
            A[row_idx, k] = x[M + row_idx - k]
    return A

def build_design_matrix_vectorized(x: np.ndarray, M: int):
    """
    Vectorized approach (using slicing) to build the same design matrix in float32.
    x is int16; cast slices to float32.
    """
    N = len(x)
    rows = N - M
    # First column of 1's in float32
    A_cols = [np.ones(rows, dtype=np.float32)]
    # Next columns are shifted versions of x, cast to float32
    for shift in range(1, M + 1):
        A_cols.append(x[M - shift : N - shift].astype(np.float32))
    A = np.column_stack(A_cols)
    return A

########################################################################
# 2) Functions to solve for coefficients (stored as float32)
########################################################################

def solve_lstsq_numpy(A: np.ndarray, y: np.ndarray):
    """
    Solve for coefficients using NumPy's lstsq solver in float32.
    Returns a 1D array of shape (M+1,) in float32.
    """
    # lstsq may do computations in float64 internally, but we can cast back
    c, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    return c.astype(np.float32)

def solve_lstsq_sklearn(A: np.ndarray, y: np.ndarray):
    """
    Solve for coefficients using scikit-learn's LinearRegression.
    (fit_intercept=False because we already have the 1-column in A).
    We store final coefficients as float32.
    """
    reg = LinearRegression(fit_intercept=False)
    reg.fit(A, y)
    # sklearn might do double precision internally; cast to float32
    return reg.coef_.astype(np.float32)

########################################################################
# 3) Functions to predict a new sequence
########################################################################

def predict_naive(coeffs: np.ndarray, seed: np.ndarray, N: int):
    """
    Naive Python prediction loop with float32 arithmetic.
    - coeffs: float32 array of shape (M+1,) => [c0, c1, ..., cM].
    - seed: last M known values (int16), but we'll cast to float32 internally.
    - N: number of output points to produce.
    The final predictions are rounded to int16.
    """
    M = len(coeffs) - 1
    # We'll store predictions in float32, then round to int16 at the end
    pred = np.zeros(N, dtype=np.float32)
    # Copy seed (cast to float32)
    pred[:M] = seed.astype(np.float32)

    # Predict forward
    for j in range(M, N):
        val = coeffs[0]
        for k in range(1, M + 1):
            val += coeffs[k] * pred[j - k]
        pred[j] = val

    # Now round to int16
    return np.round(pred).astype(np.int16)

# Optional: Numba-accelerated version
try:
    from numba import njit

    @njit
    def _predict_markov_numba(pred, coeffs, M):
        for j in range(M, len(pred)):
            val = coeffs[0]
            for k in range(1, M + 1):
                val += coeffs[k] * pred[j - k]
            pred[j] = val

    def predict_numba(coeffs: np.ndarray, seed: np.ndarray, N: int):
        """
        Numba-accelerated version of predict_naive (float32 internal arithmetic).
        Rounds final results to int16.
        """
        M = len(coeffs) - 1
        pred = np.zeros(N, dtype=np.float32)
        pred[:M] = seed.astype(np.float32)
        _predict_markov_numba(pred, coeffs, M)
        return np.round(pred).astype(np.int16)

except ImportError:
    def predict_numba(coeffs: np.ndarray, seed: np.ndarray, N: int):
        """
        Fallback if Numba is not installed: use naive approach.
        """
        print("Numba not installed. Falling back to naive prediction.")
        return predict_naive(coeffs, seed, N)

########################################################################
# 4) Main benchmarking function
########################################################################

def benchmark_markov_model(N=1_000_000, M=5, seed=0):
    """
    1) Generate random data x of length N as int16.
    2) Fit the Markov model in multiple ways:
       - Naive (build + solve) in float32
       - Vectorized+NumPy (float32)
       - Vectorized+sklearn (float32)
       Print total fitting time for each method, plus throughput in MB/s
       (using 2*N bytes as the data size).
    3) Predict a new sequence in multiple ways (naive vs numba-accelerated),
       using float32 arithmetic internally, then rounding to int16.
       Print total prediction time + throughput in MB/s.
    """
    np.random.seed(seed)
    # Generate random integers in range [-32768, 32767], but let's just do typical range
    x = np.random.randint(-30000, 30000, size=N, dtype=np.int16)

    # We define "bytes processed" as 2*N because each x_i is an int16 (2 bytes).
    bytes_processed = 2 * N
    # Build target array (still in float32 for the solver)
    # y corresponds to x[M:], but we cast to float32
    y = x[M:].astype(np.float32)

    print(f"\n=== Benchmarking Markov Model (N={N}, M={M}, data=int16, coeffs=float32) ===")

    ########################################################################
    # Fitting: Naive approach
    ########################################################################
    fit_start = time.perf_counter()

    # a) build design matrix (naive)
    t0 = time.perf_counter()
    A_naive = build_design_matrix_naive(x, M)
    dt_build_naive = time.perf_counter() - t0

    # b) solve
    t0 = time.perf_counter()
    c_naive = solve_lstsq_numpy(A_naive, y)
    dt_solve_naive = time.perf_counter() - t0

    total_naive = time.perf_counter() - fit_start

    throughput_build_naive = bytes_processed / (dt_build_naive * 1e6)
    throughput_solve_naive = bytes_processed / (dt_solve_naive * 1e6)
    throughput_total_naive = bytes_processed / (total_naive * 1e6)

    print("\n--- Fitting (Naive) ---")
    print(f"  Build matrix: {dt_build_naive:.3f}s, ~{throughput_build_naive:.2f} MB/s")
    print(f"  Solve:        {dt_solve_naive:.3f}s, ~{throughput_solve_naive:.2f} MB/s")
    print(f"  TOTAL:        {total_naive:.3f}s, ~{throughput_total_naive:.2f} MB/s")

    ########################################################################
    # Fitting: Vectorized + NumPy
    ########################################################################
    fit_start = time.perf_counter()

    # a) build design matrix (vectorized)
    t0 = time.perf_counter()
    A_vec = build_design_matrix_vectorized(x, M)
    dt_build_vec = time.perf_counter() - t0

    # b) solve
    t0 = time.perf_counter()
    c_vec = solve_lstsq_numpy(A_vec, y)
    dt_solve_vec = time.perf_counter() - t0

    total_vec = time.perf_counter() - fit_start

    throughput_build_vec = bytes_processed / (dt_build_vec * 1e6)
    throughput_solve_vec = bytes_processed / (dt_solve_vec * 1e6)
    throughput_total_vec = bytes_processed / (total_vec * 1e6)

    print("\n--- Fitting (Vectorized + NumPy) ---")
    print(f"  Build matrix: {dt_build_vec:.3f}s, ~{throughput_build_vec:.2f} MB/s")
    print(f"  Solve:        {dt_solve_vec:.3f}s, ~{throughput_solve_vec:.2f} MB/s")
    print(f"  TOTAL:        {total_vec:.3f}s, ~{throughput_total_vec:.2f} MB/s")

    ########################################################################
    # Fitting: Vectorized + scikit-learn
    ########################################################################
    fit_start = time.perf_counter()

    # We can re-use A_vec from above, but to measure a true "total time"
    # for the vectorized+sklearn path, let's rebuild it.
    t0 = time.perf_counter()
    A_vec_sklearn = build_design_matrix_vectorized(x, M)
    dt_build_vec_sklearn = time.perf_counter() - t0

    t0 = time.perf_counter()
    c_sklearn = solve_lstsq_sklearn(A_vec_sklearn, y)
    dt_solve_sklearn = time.perf_counter() - t0

    total_sklearn = time.perf_counter() - fit_start

    throughput_build_sklearn = bytes_processed / (dt_build_vec_sklearn * 1e6)
    throughput_solve_sklearn = bytes_processed / (dt_solve_sklearn * 1e6)
    throughput_total_sklearn = bytes_processed / (total_sklearn * 1e6)

    print("\n--- Fitting (Vectorized + Sklearn) ---")
    print(f"  Build matrix: {dt_build_vec_sklearn:.3f}s, ~{throughput_build_sklearn:.2f} MB/s")
    print(f"  Solve:        {dt_solve_sklearn:.3f}s, ~{throughput_solve_sklearn:.2f} MB/s")
    print(f"  TOTAL:        {total_sklearn:.3f}s, ~{throughput_total_sklearn:.2f} MB/s")

    ########################################################################
    # Prediction
    ########################################################################
    # We can pick c_vec from above as "our" coefficients for prediction.
    # We'll seed from the last M points of x (int16).
    seed_vals = x[-M:]

    # 1) Naive Prediction
    t0 = time.perf_counter()
    pred_naive = predict_naive(c_vec, seed_vals, N)
    dt_pred_naive = time.perf_counter() - t0
    throughput_pred_naive = bytes_processed / (dt_pred_naive * 1e6)

    print("\n--- Prediction (Naive) ---")
    print(f"  Predict: {dt_pred_naive:.3f}s, ~{throughput_pred_naive:.2f} MB/s")

    # Warm up Numba
    _ = predict_numba(c_vec, seed_vals, len(seed_vals) + 1)

    t0 = time.perf_counter()
    pred_numba = predict_numba(c_vec, seed_vals, N)
    dt_pred_numba = time.perf_counter() - t0
    throughput_pred_numba = bytes_processed / (dt_pred_numba * 1e6)

    print("\n--- Prediction (Numba) ---")
    print(f"  Predict: {dt_pred_numba:.3f}s, ~{throughput_pred_numba:.2f} MB/s")

    print("\n=== Done ===\n")

########################################################################
# Script entry point
########################################################################
if __name__ == "__main__":
    # Example usage
    benchmark_markov_model(N=5_000_000, M=5, seed=42)
    # Adjust N, M, and seed as needed.
