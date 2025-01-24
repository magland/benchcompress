import json
import requests
from typing import Optional

def create_signed_upload_url(url: str, size: int, user_id: str, memobin_api_key: str) -> str:
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

    file_path = url[len(prefix):]
    tempory_api_url = "https://hub.tempory.net/api/uploadFile"

    response = requests.post(
        tempory_api_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {memobin_api_key}"
        },
        json={
            "appName": "memobin",
            "filePath": file_path,
            "size": size,
            "userId": user_id
        }
    )

    if not response.ok:
        raise requests.RequestException("Failed to get signed url")

    result = response.json()
    upload_url = result["uploadUrl"]
    download_url = result["downloadUrl"]

    if download_url != url:
        raise ValueError("Mismatch between download url and url")

    return upload_url

def construct_memobin_url(alg_name: str, dataset_name: str, alg_version: str,
                         dataset_version: str, system_version: str) -> str:
    """Construct the memobin URL for a specific benchmark result.

    Args:
        alg_name: Name of the algorithm
        dataset_name: Name of the dataset
        alg_version: Version of the algorithm
        dataset_version: Version of the dataset
        system_version: Version of the system

    Returns:
        The constructed memobin URL
    """
    path = f"{alg_name}/{dataset_name}/{alg_version}/{dataset_version}/{system_version}/metadata.json"
    return f"https://tempory.net/f/memobin/{path}"

def upload_to_memobin(metadata: dict, url: str, user_id: str, memobin_api_key: str) -> None:
    """Upload metadata to memobin.

    Args:
        metadata: The metadata to upload
        url: The target URL for the file
        user_id: User ID for memobin
        memobin_api_key: API key for memobin authentication

    Raises:
        requests.RequestException: If the upload fails
    """
    metadata_bytes = json.dumps(metadata).encode('utf-8')
    size = len(metadata_bytes)

    upload_url = create_signed_upload_url(url, size, user_id, memobin_api_key)

    response = requests.put(
        upload_url,
        data=metadata_bytes,
        headers={"Content-Type": "application/json"}
    )

    if not response.ok:
        raise requests.RequestException("Failed to upload metadata to memobin")

def download_from_memobin(url: str) -> Optional[dict]:
    """Download metadata from memobin.

    Args:
        url: The URL to download from

    Returns:
        The downloaded metadata as a dictionary, or None if not found

    Raises:
        requests.RequestException: If the download fails for a reason other than 404
    """
    response = None
    try:
        response = requests.get(url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        if response and response.status_code == 404:
            return None
        raise e
