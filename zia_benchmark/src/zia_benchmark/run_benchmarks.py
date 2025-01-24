import time
import json
import os
from typing import Dict, Any, Tuple
import numpy as np
from statistics import median
from .algorithms import algorithms
from .datasets import datasets
from ._memobin import construct_memobin_url, upload_to_memobin, download_from_memobin


system_version = 'v4'

def run_benchmarks(cache_dir: str = '.benchmark_cache', verbose: bool = True) -> Dict[str, Any]:
    """Run all benchmarks, with caching based on algorithm and dataset versions.

    Results are stored in separate directories for each dataset/algorithm combination:
    cache_dir/
        dataset_name/
            algorithm_name/
                metadata.json  # Contains algorithm version, dataset version, and results
                compressed.dat # The actual compressed data

    Args:
        cache_dir: Directory to store cached results

    Returns:
        Dictionary containing benchmark results and metadata
    """
    print("\n=== Starting Benchmark Run ===")
    print(f"Cache directory: {cache_dir}")

    os.makedirs(cache_dir, exist_ok=True)

    results = []
    print("\nRunning benchmarks for all dataset-algorithm combinations...")

    # Run benchmarks for each dataset and algorithm combination
    for dataset in datasets:
        print(f"\n--- Dataset: {dataset['name']} ---")
        # Create dataset once for all algorithms
        data = dataset['create']()
        dtype = str(data.dtype)
        original_size = len(data.tobytes())
        print(f"Created dataset: shape={data.shape}, dtype={dtype}")
        print(f"Original size: {original_size:,} bytes")

        for algorithm in algorithms:
            alg_name = algorithm['name']
            print(f"\nTesting algorithm: {alg_name}")

            # Check if we can use cached result
            test_dir = os.path.join(cache_dir, dataset['name'], alg_name)
            metadata_file = os.path.join(test_dir, 'metadata.json')
            compressed_file = os.path.join(test_dir, 'compressed.dat')

            # First try local cache
            cached_data = None
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r') as f:
                    cached_data = json.load(f)
                    # if versions do not match, then set to None
                    if (
                        cached_data['result']['algorithm_version'] != algorithm['version'] or
                        cached_data['result']['dataset_version'] != dataset['version'] or
                        cached_data['result'].get('system_version', '') != system_version
                    ):
                        cached_data = None

            # If not in local cache, try memobin
            if cached_data is None:
                memobin_url = construct_memobin_url(
                    alg_name, dataset['name'],
                    algorithm['version'], dataset['version'],
                    system_version
                )
                if verbose:
                    print("  Looking for cached result in memobin...")
                cached_data = download_from_memobin(memobin_url)
                if cached_data is not None:
                    if verbose:
                        print("  Found result in memobin, saving locally...")
                    # Save to local cache
                    os.makedirs(test_dir, exist_ok=True)
                    with open(metadata_file, 'w') as f:
                        json.dump(cached_data, f, indent=2)

            if cached_data is not None and (
                cached_data['result']['algorithm_version'] == algorithm['version'] and
                cached_data['result']['dataset_version'] == dataset['version'] and
                cached_data['result'].get('system_version', '') == system_version
            ):
                print("  Using cached result:")
                results.append(cached_data['result'])
                continue

            print("  Running new benchmark...")

            def run_timed_trials(operation, *args) -> Tuple[float, float]:
                """Run multiple trials of an operation until total time exceeds 1 second.
                Returns (median_time, mb_per_sec)"""
                times = []
                total_time = 0
                array_size_mb = data.nbytes / (1024 * 1024)  # Convert to MB

                while total_time < 1.0:
                    start_time = time.perf_counter()
                    _ = operation(*args)  # Execute operation but discard result
                    trial_time = time.perf_counter() - start_time
                    times.append(trial_time)
                    total_time += trial_time

                median_time = median(times)
                mb_per_sec = array_size_mb / median_time
                return median_time, mb_per_sec

            # Measure encoding with multiple trials
            encode_time, encode_mb_per_sec = run_timed_trials(algorithm['encode'], data)
            encoded = algorithm['encode'](data)  # One final encode to get the result
            compressed_size = len(encoded)
            compression_ratio = original_size / compressed_size
            print("  Compression complete:")
            print(f"    Compressed size: {compressed_size:,} bytes")
            print(f"    Compression ratio: {compression_ratio:.2f}x")
            print(f"    Encode time: {encode_time*1000:.2f}ms")
            print(f"    Encode throughput: {encode_mb_per_sec:.2f} MB/s")

            print("  Verifying decompression...")
            # Measure decoding with multiple trials
            decode_time, decode_mb_per_sec = run_timed_trials(algorithm['decode'], encoded, dtype)
            decoded = algorithm['decode'](encoded, dtype)  # One final decode to verify
            print(f"    Decode time: {decode_time*1000:.2f}ms")
            print(f"    Decode throughput: {decode_mb_per_sec:.2f} MB/s")

            # Verify correctness
            if not np.array_equal(data, decoded):
                raise ValueError(
                    f"Decompression verification failed for {alg_name} on {dataset['name']}"
                )
            print("  Verification successful!")

            # Store result
            result = {
                'dataset': dataset['name'],
                'algorithm': alg_name,
                'algorithm_version': algorithm['version'],
                'dataset_version': dataset['version'],
                'system_version': system_version,
                'compression_ratio': compression_ratio,
                'encode_time': encode_time,
                'decode_time': decode_time,
                'encode_mb_per_sec': encode_mb_per_sec,
                'decode_mb_per_sec': decode_mb_per_sec,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'array_shape': data.shape,
                'array_dtype': dtype,
                'timestamp': time.time()
            }
            results.append(result)

            # Save result and compressed data
            os.makedirs(test_dir, exist_ok=True)
            cache_data = {
                'result': result
            }
            with open(metadata_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
            with open(compressed_file, 'wb') as f:
                f.write(encoded)
            print(f"  Results saved to: {test_dir}")

            # Upload to memobin if API key is set and upload is enabled
            memobin_api_key = os.environ.get('MEMOBIN_API_KEY')
            upload_enabled = os.environ.get('UPLOAD_TO_MEMOBIN') == '1'
            if memobin_api_key and upload_enabled:
                if verbose:
                    print("  Uploading results to memobin...")
                try:
                    memobin_url = construct_memobin_url(
                        alg_name, dataset['name'],
                        algorithm['version'], dataset['version'],
                        system_version
                    )
                    upload_to_memobin(
                        cache_data,
                        memobin_url,
                        os.environ.get('MEMOBIN_USER_ID', 'default'),
                        memobin_api_key
                    )
                    if verbose:
                        print("  Successfully uploaded to memobin")
                except Exception as e:
                    print(f"  Warning: Failed to upload to memobin: {str(e)}")

    print("\n=== Benchmark Run Complete ===\n")
    return {'results': results}
