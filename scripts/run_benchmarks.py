#!/usr/bin/env python3

import json
from pathlib import Path
import zia_benchmark

def format_size(size_bytes: float) -> str:
    """Format size in bytes to human readable string"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def format_time(seconds: float) -> str:
    """Format time in seconds to human readable string"""
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.1f} µs"
    if seconds < 1:
        return f"{seconds * 1_000:.1f} ms"
    return f"{seconds:.2f} s"

def main():
    # Run benchmarks
    print("Running benchmarks...")
    results = zia_benchmark.run_benchmarks()

    # Group results by dataset
    datasets = {}
    for result in results['results']:
        dataset_name = result['dataset']
        if dataset_name not in datasets:
            datasets[dataset_name] = []
        datasets[dataset_name].append(result)

    # Print results
    print("\nBenchmark Results:")
    print("=================")

    for dataset_name, dataset_results in sorted(datasets.items()):
        print(f"\nDataset: {dataset_name}")
        print("-" * (len(dataset_name) + 9))
        print(f"Original size: {format_size(dataset_results[0]['original_size'])}")

        # Sort algorithms by compression ratio
        dataset_results.sort(key=lambda x: x['compression_ratio'], reverse=True)

        # Print table header
        print("\n{:<15} {:>12} {:>12} {:>12}".format(
            "Algorithm", "Ratio", "Encode", "Decode"
        ))
        print("-" * 53)

        # Print results for each algorithm
        for result in dataset_results:
            print("{:<15} {:>11.2f}x {:>12} {:>12}".format(
                result['algorithm'],
                result['compression_ratio'],
                format_time(result['encode_time']),
                format_time(result['decode_time'])
            ))

    # Save detailed results to JSON
    output_dir = Path("benchmark_results")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "results.json"

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nDetailed results saved to {output_file}")

if __name__ == "__main__":
    main()
