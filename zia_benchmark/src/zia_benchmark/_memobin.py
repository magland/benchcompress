import json
import requests
from typing import Optional


def create_signed_upload_url(
    url: str, size: int, user_id: str, memobin_api_key: str
) -> str:
    """Create a signed upload URL for memobin.

    Args:
        url: The target URL for the file
        size: Size of the file in bytes
        user_id: User ID for memobin
        memobin_api_key: API key for memobin authentication

    Returns:
        The signed upload URL

    Raises:
        ValueError: If the URL prefix is invalid
        requests.RequestException: If the API request fails
    """
    prefix = "https://tempory.net/f/memobin/"
    if not url.startswith(prefix):
        raise ValueError("Invalid url. Does not have proper prefix")

    file_path = url[len(prefix) :]
    tempory_api_url = "https://hub.tempory.net/api/uploadFile"

    response = requests.post(
        tempory_api_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {memobin_api_key}",
        },
        json={
            "appName": "memobin",
            "filePath": file_path,
            "size": size,
            "userId": user_id,
        },
    )

    if not response.ok:
        raise requests.RequestException("Failed to get signed url")

    result = response.json()
    upload_url = result["uploadUrl"]
    download_url = result["downloadUrl"]

    if download_url != url:
        raise ValueError("Mismatch between download url and url")

    return upload_url


def construct_memobin_url(
    alg_name: str,
    dataset_name: str,
    alg_version: str,
    dataset_version: str,
    system_version: str,
    file_type: str = "metadata.json",
) -> str:
    """Construct the memobin URL for a specific benchmark result or dataset.

    Args:
        alg_name: Name of the algorithm
        dataset_name: Name of the dataset
        alg_version: Version of the algorithm
        dataset_version: Version of the dataset
        system_version: Version of the system
        file_type: Type of file (metadata.json or data.bin)

    Returns:
        The constructed memobin URL
    """
    path = f"{alg_name}/{dataset_name}/{alg_version}/{dataset_version}/{system_version}/{file_type}"
    return f"https://tempory.net/f/memobin/{path}"


def construct_dataset_url(
    dataset_name: str, dataset_version: str, format: str = "dat"
) -> str:
    """Construct the memobin URL for a dataset.

    Args:
        dataset_name: Name of the dataset
        dataset_version: Version of the dataset
        format: File format ("dat", "npy", or "json")

    Returns:
        The constructed memobin URL for the dataset
    """
    path = f"datasets/{dataset_name}/{dataset_version}/{dataset_name}-{dataset_version}.{format}"
    return f"https://tempory.net/f/memobin/{path}"


def upload_to_memobin(
    data: dict | bytes,
    url: str,
    memobin_api_key: str,
    content_type: str = "application/json",
) -> None:
    """Upload data to memobin.

    Args:
        data: The data to upload (dict for JSON or bytes for binary)
        url: The target URL for the file
        memobin_api_key: API key for memobin authentication
        content_type: Content type of the data

    Raises:
        requests.RequestException: If the upload fails
    """
    if isinstance(data, dict):
        data_bytes = json.dumps(data).encode("utf-8")
    else:
        data_bytes = data
    size = len(data_bytes)

    upload_url = create_signed_upload_url(url, size, 'zia', memobin_api_key)

    response = requests.put(
        upload_url, data=data_bytes, headers={"Content-Type": content_type}
    )

    if not response.ok:
        raise requests.RequestException("Failed to upload data to memobin")


def exists_in_memobin(url: str) -> bool:
    """Check if a file exists in memobin using a HEAD request.

    Args:
        url: The URL to check

    Returns:
        True if the file exists, False otherwise
    """
    try:
        response = requests.head(url)
        return (
            200 <= response.status_code < 300
        )  # Any 2xx status code indicates success
    except requests.RequestException:
        return False


def download_from_memobin(url: str, as_json: bool = True) -> Optional[dict | bytes]:
    """Download data from memobin.

    Args:
        url: The URL to download from
        as_json: Whether to parse the response as JSON

    Returns:
        The downloaded data as a dictionary or bytes, or None if not found

    Raises:
        requests.RequestException: If the download fails for a reason other than 404
    """
    response = None
    try:
        response = requests.get(url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json() if as_json else response.content
    except requests.RequestException as e:
        if response and response.status_code == 404:
            return None
        raise e
