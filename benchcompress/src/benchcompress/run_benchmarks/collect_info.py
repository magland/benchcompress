from typing import List, Dict, Any
from ._memobin import construct_dataset_url

GITHUB_ALGORITHMS_PREFIX = "https://github.com/magland/benchcompress/blob/main/benchcompress/src/benchcompress/algorithms/"
GITHUB_DATASETS_PREFIX = "https://github.com/magland/benchcompress/blob/main/benchcompress/src/benchcompress/datasets/"


def collect_algorithm_info(algorithms: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Collect information about compression algorithms.

    Args:
        algorithms: List of algorithm dictionaries

    Returns:
        List of algorithm information dictionaries
    """
    algorithm_info = []
    for algorithm in algorithms:
        info = {
            "name": algorithm["name"],
            "description": algorithm.get("description", ""),
            "long_description": algorithm.get("long_description", ""),
            "version": algorithm["version"],
            "tags": algorithm.get("tags", []),
        }
        if "source_file" in algorithm:
            info["source_file"] = GITHUB_ALGORITHMS_PREFIX + algorithm["source_file"]
        algorithm_info.append(info)
    return algorithm_info


def collect_dataset_info(datasets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Collect information about benchmark datasets.

    Args:
        datasets: List of dataset dictionaries

    Returns:
        List of dataset information dictionaries
    """
    dataset_info = []
    for dataset in datasets:
        info = {
            "name": dataset["name"],
            "description": dataset.get("description", ""),
            "long_description": dataset.get("long_description", ""),
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
    return dataset_info
