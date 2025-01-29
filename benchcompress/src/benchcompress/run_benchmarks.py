import time
import json
import os
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime
import numpy as np
from statistics import median
from .algorithms import algorithms
from .datasets import datasets
from ._memobin import (
    construct_memobin_url,
    construct_dataset_url,
    upload_to_memobin,
    download_from_memobin,
    exists_in_memobin,
)


system_version = "v6"
GITHUB_ALGORITHMS_PREFIX = "https://github.com/magland/benchcompress/blob/main/benchcompress/src/benchcompress/algorithms/"
GITHUB_DATASETS_PREFIX = "https://github.com/magland/benchcompress/blob/main/benchcompress/src/benchcompress/datasets/"


def is_compatible(algorithm_tags: List[str], dataset_tags: List[str]) -> bool:
    """Check if an algorithm is compatible with a dataset based on their tags.

    Args:
        algorithm_tags: List of tags for the algorithm
        dataset_tags: List of tags for the dataset

    Returns:
        True if the algorithm should be applied to the dataset
    """
    # If algorithm has delta_encoding or markov_prediction, dataset must have continuous, timeseries, 1d
    if "delta_encoding" in algorithm_tags or "markov_prediction" in algorithm_tags:
        if (
            "continuous" not in dataset_tags
            or "timeseries" not in dataset_tags
            or "1d" not in dataset_tags
        ):
            return False

    # If algorithm has zero_rle, dataset must have sparse, timeseries, 1d
    if "zero_rle" in algorithm_tags:
        if (
            "sparse" not in dataset_tags
            or "timeseries" not in dataset_tags
            or "1d" not in dataset_tags
        ):
            return False

    # If algorithm has integer, dataset must have integer
    if "integer" in algorithm_tags:
        if "integer" not in dataset_tags:
            return False

    return True


def upload_benchmark_status(
    memobin_api_key: str,
    current_dataset: str,
    current_algorithm: str,
    completed_benchmarks: List[Dict[str, Any]],
    total_benchmarks: int,
    start_time: float,
) -> None:
    """Upload current benchmark status to memobin.

    Args:
        memobin_api_key: API key for memobin authentication
        current_dataset: Name of the current dataset being processed
        current_algorithm: Name of the current algorithm being tested
        completed_benchmarks: List of completed benchmark results
        total_benchmarks: Total number of benchmarks to run
        start_time: Timestamp when the benchmark run started
    """
    status = {
        "current_dataset": current_dataset,
        "current_algorithm": current_algorithm,
        "completed_count": len(completed_benchmarks),
        "total_count": total_benchmarks,
        "progress_percentage": (len(completed_benchmarks) / total_benchmarks) * 100,
        "elapsed_time": time.time() - start_time,
        "last_update": datetime.now().isoformat(),
        "completed_benchmarks": completed_benchmarks,
    }

    status_url = "https://tempory.net/f/memobin/benchmark_status/current.json"
    upload_to_memobin(status, status_url, memobin_api_key)


def run_benchmarks(
    cache_dir: str = ".benchmark_cache",
    verbose: bool = True,
    selected_algorithms: Optional[List[dict]] = None,
    selected_datasets: Optional[List[dict]] = None,
    force: bool = False,
) -> Dict[str, Any]:
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

    start_time = time.time()
    last_status_upload = 0  # Track last status upload time
    results = []
    print("\nRunning benchmarks for all dataset-algorithm combinations...")

    # Use selected datasets/algorithms or fall back to all
    datasets_to_run = selected_datasets if selected_datasets is not None else datasets
    algorithms_to_run = (
        selected_algorithms if selected_algorithms is not None else algorithms
    )

    # Calculate total number of benchmarks
    total_benchmarks = sum(
        1
        for dataset in datasets_to_run
        for algorithm in algorithms_to_run
        if is_compatible(algorithm.get("tags", []), dataset.get("tags", []))
    )

    # Run benchmarks for each dataset and algorithm combination
    memobin_api_key = os.environ.get("MEMOBIN_API_KEY")
    upload_enabled = os.environ.get("UPLOAD_TO_MEMOBIN") == "1"

    for dataset in datasets_to_run:
        dataset_tags = dataset.get("tags", [])
        print(f"\n*** Dataset: {dataset['name']} (tags: {dataset_tags}) ***")

        # only create the dataset if it is needed
        data = None

        for algorithm in algorithms_to_run:
            alg_name = algorithm["name"]
            alg_tags = algorithm.get("tags", [])

            # Skip if algorithm and dataset are not compatible based on tags
            if not is_compatible(alg_tags, dataset_tags):
                if verbose:
                    print(
                        f"\nSkipping algorithm {alg_name} (tags: {alg_tags}) - incompatible with dataset tags"
                    )
                continue

            print(f"\nTesting algorithm: {alg_name} (tags: {alg_tags})")

            # Upload current status to memobin if enabled (once per minute)
            current_time = time.time()
            if (
                memobin_api_key
                and upload_enabled
                and (current_time - last_status_upload >= 60)
            ):  # Check if 60 seconds have passed
                try:
                    upload_benchmark_status(
                        memobin_api_key,
                        dataset["name"],
                        alg_name,
                        results,
                        total_benchmarks,
                        start_time,
                    )
                    last_status_upload = current_time  # Update last upload time
                except Exception as e:
                    print(f"  Warning: Failed to upload status to memobin: {str(e)}")

            # Check if we can use cached result (unless force flag is set)
            test_dir = os.path.join(cache_dir, dataset["name"], alg_name)
            metadata_file = os.path.join(test_dir, "metadata.json")
            compressed_file = os.path.join(test_dir, "compressed.dat")

            # First try local cache (unless force flag is set)
            cached_data = None
            if not force and os.path.exists(metadata_file):
                with open(metadata_file, "r") as f:
                    cached_data = json.load(f)
                    # if versions do not match, then set to None
                    if isinstance(cached_data, dict) and "result" in cached_data:
                        result = cached_data["result"]
                        if (
                            result["algorithm_version"] != algorithm["version"]
                            or result["dataset_version"] != dataset["version"]
                            or result.get("system_version", "") != system_version
                        ):
                            cached_data = None

            # If not in local cache, try memobin (unless force flag is set)
            if cached_data is None and not force:
                memobin_url = construct_memobin_url(
                    alg_name,
                    dataset["name"],
                    algorithm["version"],
                    dataset["version"],
                    system_version,
                    "metadata.json",
                )
                if verbose:
                    print("  Looking for cached result in memobin...")
                cached_data = download_from_memobin(memobin_url)
                if cached_data is not None:
                    if verbose:
                        print("  Found result in memobin, saving locally...")
                    # Save to local cache
                    os.makedirs(test_dir, exist_ok=True)
                    with open(metadata_file, "w") as f:
                        json.dump(cached_data, f, indent=2)

            if (
                cached_data is not None
                and isinstance(cached_data, dict)
                and "result" in cached_data
            ):
                result = cached_data["result"]
                if (
                    isinstance(result, dict)
                    and result.get("algorithm_version") == algorithm["version"]
                    and result.get("dataset_version") == dataset["version"]
                    and result.get("system_version", "") == system_version
                ):
                    print("  Using cached result:")
                    result["cache_status"] = "cached"
                    results.append(result)
                    continue

            print(f"  Running benchmark for {alg_name} on {dataset['name']}...")
            if data is None:
                data = dataset["create"]()
                print(f"Created dataset: shape={data.shape}, dtype={data.dtype}")
            else:
                print("Dataset already created")
            dtype = str(data.dtype)
            original_size = len(data.tobytes())
            print(f"Dataset: shape={data.shape}, dtype={dtype}")
            print(f"Original size: {original_size:,} bytes")

            # Upload dataset to memobin if enabled
            memobin_api_key = os.environ.get("MEMOBIN_API_KEY")
            upload_enabled = os.environ.get("UPLOAD_TO_MEMOBIN") == "1"
            if memobin_api_key and upload_enabled:
                try:
                    # Upload array metadata as JSON
                    dataset_url_json = construct_dataset_url(
                        dataset["name"], dataset["version"], "json"
                    )
                    if not exists_in_memobin(dataset_url_json):
                        if verbose:
                            print("  Uploading dataset metadata to memobin...")
                        metadata = {"dtype": str(data.dtype), "shape": data.shape}
                        upload_to_memobin(
                            metadata,
                            dataset_url_json,
                            memobin_api_key,
                            content_type="application/json",
                        )
                        if verbose:
                            print("  Successfully uploaded metadata")

                    # Upload raw .dat format
                    dataset_url_raw = construct_dataset_url(
                        dataset["name"], dataset["version"], "dat"
                    )
                    if not exists_in_memobin(dataset_url_raw):
                        if verbose:
                            print("  Uploading dataset (raw) to memobin...")
                        upload_to_memobin(
                            data.tobytes(),
                            dataset_url_raw,
                            memobin_api_key,
                            content_type="application/octet-stream",
                        )
                        if verbose:
                            print("  Successfully uploaded raw dataset")

                    # Upload .npy format
                    dataset_url_npy = construct_dataset_url(
                        dataset["name"], dataset["version"], "npy"
                    )
                    if not exists_in_memobin(dataset_url_npy):
                        if verbose:
                            print("  Uploading dataset (npy) to memobin...")
                        # Save array to a temporary .npy file
                        temp_npy = os.path.join(cache_dir, "temp.npy")
                        np.save(temp_npy, data)
                        with open(temp_npy, "rb") as f:
                            npy_bytes = f.read()
                        os.remove(temp_npy)  # Clean up temp file

                        upload_to_memobin(
                            npy_bytes,
                            dataset_url_npy,
                            memobin_api_key,
                            content_type="application/octet-stream",
                        )
                        if verbose:
                            print("  Successfully uploaded npy dataset")
                except Exception as e:
                    print(f"  Warning: Failed to upload dataset to memobin: {str(e)}")

            assert data is not None
            assert isinstance(data, np.ndarray)
            assert isinstance(original_size, int)
            assert isinstance(dtype, str)

            def run_timed_trials(operation, *args) -> Tuple[float, float, Any]:
                """Run multiple trials of an operation until total time exceeds 1 second.
                Returns (median_time, mb_per_sec)"""
                assert data is not None
                assert isinstance(data, np.ndarray)
                times = []
                total_time = 0
                array_size_mb = data.nbytes / (1024 * 1024)  # Convert to MB

                ret = None
                while total_time < 1.0:
                    start_time = time.perf_counter()
                    ret = operation(*args)  # Execute operation but discard result
                    trial_time = time.perf_counter() - start_time
                    times.append(trial_time)
                    total_time += trial_time

                median_time = median(times)
                mb_per_sec = array_size_mb / median_time
                return median_time, mb_per_sec, ret

            print("  Encoding...")
            encode_time, encode_mb_per_sec, encoded = run_timed_trials(
                algorithm["encode"], data
            )
            compressed_size = len(encoded)
            compression_ratio = original_size / compressed_size
            print("  Compression complete:")
            print(f"    Compressed size: {compressed_size:,} bytes")
            print(f"    Compression ratio: {compression_ratio:.2f}x")
            print(f"    Encode time: {encode_time*1000:.2f}ms")
            print(f"    Encode throughput: {encode_mb_per_sec:.2f} MB/s")

            print("  Decoding...")
            # Measure decoding with multiple trials
            decode_time, decode_mb_per_sec, decoded = run_timed_trials(
                algorithm["decode"], encoded, dtype, data.shape
            )
            print(f"    Decode time: {decode_time*1000:.2f}ms")
            print(f"    Decode throughput: {decode_mb_per_sec:.2f} MB/s")

            if len(data) != len(decoded):
                raise ValueError(
                    f"Decompression failed: decoded length {len(decoded)} != original length {len(data)}"
                )

            # Verify correctness
            if not np.array_equal(data, decoded):
                print(data[:100])
                print(decoded[:100])
                for j in range(len(data)):
                    if data[j] != decoded[j]:
                        print(f"Error at index {j}: {data[j]} != {decoded[j]}")
                raise ValueError(
                    f"Decompression verification failed for {alg_name} on {dataset['name']}"
                )
            print("  Verification successful!")

            # Store result
            result = {
                "dataset": dataset["name"],
                "algorithm": alg_name,
                "algorithm_version": algorithm["version"],
                "dataset_version": dataset["version"],
                "system_version": system_version,
                "compression_ratio": compression_ratio,
                "encode_time": encode_time,
                "decode_time": decode_time,
                "encode_mb_per_sec": encode_mb_per_sec,
                "decode_mb_per_sec": decode_mb_per_sec,
                "original_size": original_size,
                "compressed_size": compressed_size,
                "array_shape": data.shape,
                "array_dtype": dtype,
                "timestamp": time.time(),
                "cache_status": "new",
            }
            results.append(result)

            # Save result and compressed data
            os.makedirs(test_dir, exist_ok=True)
            cache_data = {"result": result}
            with open(metadata_file, "w") as f:
                json.dump(cache_data, f, indent=2)
            with open(compressed_file, "wb") as f:
                f.write(encoded)
            print(f"  Results saved to: {test_dir}")

            # Upload to memobin if API key is set and upload is enabled
            memobin_api_key = os.environ.get("MEMOBIN_API_KEY")
            upload_enabled = os.environ.get("UPLOAD_TO_MEMOBIN") == "1"
            if memobin_api_key and upload_enabled:
                if verbose:
                    print("  Uploading results to memobin...")
                try:
                    memobin_url = construct_memobin_url(
                        alg_name,
                        dataset["name"],
                        algorithm["version"],
                        dataset["version"],
                        system_version,
                    )
                    upload_to_memobin(
                        cache_data,
                        memobin_url,
                        memobin_api_key,
                    )
                    if verbose:
                        print("  Successfully uploaded to memobin")
                except Exception as e:
                    print(f"  Warning: Failed to upload to memobin: {str(e)}")

    print("\n=== Benchmark Run Complete ===\n")

    # Collect algorithm and dataset information as lists
    algorithm_info = []
    for algorithm in algorithms:
        info = {
            "name": algorithm["name"],
            "description": algorithm.get("description", ""),
            "version": algorithm["version"],
            "tags": algorithm.get("tags", []),
        }
        if "source_file" in algorithm:
            info["source_file"] = GITHUB_ALGORITHMS_PREFIX + algorithm["source_file"]
        algorithm_info.append(info)

    dataset_info = []
    for dataset in datasets:
        info = {
            "name": dataset["name"],
            "description": dataset.get("description", ""),
            "version": dataset["version"],
            "tags": dataset.get("tags", []),
            "data_url_raw": construct_dataset_url(
                dataset["name"], dataset["version"], "dat"
            ),
            "data_url_npy": construct_dataset_url(
                dataset["name"], dataset["version"], "npy"
            ),
            "data_url_json": construct_dataset_url(
                dataset["name"], dataset["version"], "json"
            ),
        }
        if "source_file" in dataset:
            info["source_file"] = GITHUB_DATASETS_PREFIX + dataset["source_file"]
        dataset_info.append(info)

    return {"results": results, "algorithms": algorithm_info, "datasets": dataset_info}
