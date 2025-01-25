/*************************************************
 * markov_bench.cpp
 *
 * A C++ program demonstrating:
 *   1. Generating int16_t data (size N).
 *   2. Building a design matrix in float32.
 *   3. Solving for coefficients in float32 with Eigen.
 *   4. Predicting a new sequence (float32 -> round to int16_t).
 *   5. Measuring times & throughput (MB/s).
 *
 * Requires Eigen for linear algebra:
 *   https://eigen.tuxfamily.org/
 *************************************************/

#include <Eigen/Dense>
#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <cmath>
#include <cstdint>

//---------------------------------------------------------------------------
// 1) Helper for timing
//---------------------------------------------------------------------------
inline double secondsBetween(
    const std::chrono::high_resolution_clock::time_point& start,
    const std::chrono::high_resolution_clock::time_point& end)
{
    return std::chrono::duration<double>(end - start).count();
}

//---------------------------------------------------------------------------
// 2) Generate random int16_t data
//    We create N random integers in [-30000, 30000].
//---------------------------------------------------------------------------
std::vector<int16_t> generateData(std::size_t N, unsigned seed = 0)
{
    std::mt19937_64 rng(seed);
    std::uniform_int_distribution<int> dist(-30000, 30000);

    std::vector<int16_t> x(N);
    for (std::size_t i = 0; i < N; ++i) {
        x[i] = static_cast<int16_t>(dist(rng));
    }
    return x;
}

//---------------------------------------------------------------------------
// 3) Build the design matrix A (float32) in a naive manner.
//
//    For a Markov model of order M, we want rows for j in [M..N-1]:
//       [1, x_{j-1}, x_{j-2}, ..., x_{j-M} ]
//    We'll store these in A, shape: (N - M) x (M + 1).
//---------------------------------------------------------------------------
Eigen::MatrixXf buildDesignMatrixNaive(const std::vector<int16_t>& x, std::size_t M)
{
    const std::size_t N = x.size();
    const std::size_t rows = N - M;
    const std::size_t cols = M + 1;

    Eigen::MatrixXf A(rows, cols);  // float32

    // Fill A
    for (std::size_t row = 0; row < rows; ++row) {
        // First column = 1.0
        A(row, 0) = 1.0f;
        // Next columns: x_{(row + M) - k}, for k=1..M
        for (std::size_t k = 1; k <= M; ++k) {
            int16_t val = x[(row + M) - k];
            A(row, k) = static_cast<float>(val); // int16 -> float32
        }
    }

    return A;
}

//---------------------------------------------------------------------------
// 4) Solve for coefficients c in float32 using Eigen's SVD.
//
//    c = argmin_c ||A c - y||^2
//    We store and return c as Eigen::VectorXf (float32).
//---------------------------------------------------------------------------
Eigen::VectorXf solveCoeffsEigen(const Eigen::MatrixXf& A, const Eigen::VectorXf& y)
{
    // SVD-based solve (ComputeThinU|V for full solution in least-squares sense)
    // Alternatively: A.colPivHouseholderQr().solve(y), etc.
    Eigen::VectorXf c = A.bdcSvd(Eigen::ComputeThinU | Eigen::ComputeThinV).solve(y);
    return c;
}

//---------------------------------------------------------------------------
// 5) Predict a new sequence using naive float32 arithmetic and round to int16_t.
//
//    - coeffs: c0..cM  (length M+1)
//    - seed:   last M real data points (int16_t)
//    - Output: N predicted points, as int16_t.
//
//    predicted[j] = c0 + c1*predicted[j-1] + ... + cM*predicted[j-M]
//---------------------------------------------------------------------------
std::vector<int16_t> predictNaive(
    const Eigen::VectorXf& coeffs,
    const std::vector<int16_t>& seed,
    std::size_t N)
{
    std::size_t M = coeffs.size() - 1; // since c has M+1 entries
    std::vector<float> predFloat(N, 0.0f);  // store intermediate in float32
    std::vector<int16_t> predInt(N, 0);     // final integer output

    // Initialize first M from seed (cast to float)
    for (std::size_t i = 0; i < M; ++i) {
        predFloat[i] = static_cast<float>(seed[i]);
    }

    // Predict forward
    for (std::size_t j = M; j < N; ++j) {
        float val = coeffs(0); // c0
        for (std::size_t k = 1; k <= M; ++k) {
            val += coeffs(k) * predFloat[j - k];
        }
        predFloat[j] = val;
    }

    // Round to int16_t
    for (std::size_t i = 0; i < N; ++i) {
        float r = std::round(predFloat[i]);
        // clamp into int16 range if you want to be safe, but ignoring extremes here:
        if (r > 32767.f) r = 32767.f;
        if (r < -32768.f) r = -32768.f;
        predInt[i] = static_cast<int16_t>(r);
    }

    return predInt;
}

//---------------------------------------------------------------------------
// 6) Main benchmark function
//---------------------------------------------------------------------------
int main()
{
    // Parameters
    std::size_t N = 5*1000*1000;
    std::size_t M = 5;
    unsigned seed = 42;

    // Generate data
    auto startAll = std::chrono::high_resolution_clock::now();
    auto x = generateData(N, seed);
    auto endAll = std::chrono::high_resolution_clock::now();
    double dtGen = secondsBetween(startAll, endAll);

    // We'll define "bytes processed" as 2*N for throughput (since int16_t=2 bytes).
    double bytesProcessed = double(2 * N);

    std::cout << "\n=== C++ Markov Model Benchmark ===\n"
              << "N=" << N << ", M=" << M << ", data=int16_t, coeffs=float32\n\n";

    std::cout << "Data generation: " << dtGen << " s\n";

    //----------------------------------------------------------------------
    // Build design matrix (naive)
    //----------------------------------------------------------------------
    auto t0 = std::chrono::high_resolution_clock::now();
    Eigen::MatrixXf A = buildDesignMatrixNaive(x, M);
    auto t1 = std::chrono::high_resolution_clock::now();
    double dtBuild = secondsBetween(t0, t1);

    // Prepare y (float32) = x[M..N-1]
    // We'll store it in an Eigen vector
    std::size_t rows = N - M;
    Eigen::VectorXf y(rows);
    for (std::size_t i = 0; i < rows; ++i) {
        y(i) = static_cast<float>(x[i + M]);
    }

    //----------------------------------------------------------------------
    // Solve for coefficients
    //----------------------------------------------------------------------
    auto t2 = std::chrono::high_resolution_clock::now();
    Eigen::VectorXf coeffs = solveCoeffsEigen(A, y);
    auto t3 = std::chrono::high_resolution_clock::now();
    double dtSolve = secondsBetween(t2, t3);

    double dtFittingTotal = dtBuild + dtSolve;

    double buildThroughput = bytesProcessed / (dtBuild * 1.0e6);
    double solveThroughput = bytesProcessed / (dtSolve * 1.0e6);
    double totalThroughput = bytesProcessed / (dtFittingTotal * 1.0e6);

    std::cout << "--- Fitting (Naive build + Eigen solve) ---\n";
    std::cout << "  Build matrix: " << dtBuild << " s, ~" << buildThroughput << " MB/s\n";
    std::cout << "  Solve:        " << dtSolve << " s, ~" << solveThroughput << " MB/s\n";
    std::cout << "  TOTAL:        " << dtFittingTotal << " s, ~" << totalThroughput << " MB/s\n";

    //----------------------------------------------------------------------
    // Prediction
    //----------------------------------------------------------------------
    // We'll seed from the last M points of x
    std::vector<int16_t> seedVals(M);
    for (std::size_t i = 0; i < M; ++i) {
        seedVals[i] = x[N - M + i];
    }

    auto t4 = std::chrono::high_resolution_clock::now();
    auto predictions = predictNaive(coeffs, seedVals, N);
    auto t5 = std::chrono::high_resolution_clock::now();
    double dtPredict = secondsBetween(t4, t5);
    double predThroughput = bytesProcessed / (dtPredict * 1.0e6);

    std::cout << "\n--- Prediction (Naive float32 -> round int16) ---\n";
    std::cout << "  Predict: " << dtPredict << " s, ~" << predThroughput << " MB/s\n";

    //----------------------------------------------------------------------
    // Done
    //----------------------------------------------------------------------
    std::cout << "\n=== Done ===\n\n";

    return 0;
}
