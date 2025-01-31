#!/usr/bin/env python

"""
This script prepares a seismic dataset from Lim et al. 2024 for use in the benchcompress project.
It downloads seismic waveform data from Zenodo, extracts .sac files from a specific folder,
and concatenates them into a single numpy array. The resulting dataset will be used to evaluate
various compression algorithms in benchcompress to determine their effectiveness on real-world
seismic waveform data.

The original data is from:
Lim, H., & Zhang, M. (2024). Machine Learning Phase Picker Training Dataset in Shanghai.
Zenodo. https://doi.org/10.5281/zenodo.10457508
"""

import os
import sys
from urllib.request import urlretrieve
import tarfile
import glob
from obspy import read
import numpy as np

def download_file(url, local_filename):
    if os.path.exists(local_filename):
        print(f"File {local_filename} already exists locally")
        return True

    print(f"Downloading {url} to {local_filename}...")
    try:
        urlretrieve(url, local_filename)
        print("Download completed successfully")
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

def extract_data_folder(archive_path):
    if not os.path.exists(archive_path):
        print(f"Archive file {archive_path} not found")
        return False

    print(f"Extracting /data/01 folder from {archive_path}...")
    try:
        with tarfile.open(archive_path, 'r:gz') as tar:
            # Extract only files in the /data/01 directory
            members = [m for m in tar.getmembers() if m.name.startswith('data/01/')]
            for member in members:
                tar.extract(member)
        print("Extraction completed successfully")
        return True
    except Exception as e:
        print(f"Error extracting archive: {e}")
        return False

def load_and_concatenate_sac_files(directory):
    # Find all .sac files in the directory
    sac_files = glob.glob(f"{directory}/*.sac")
    if not sac_files:
        print(f"No .sac files found in {directory}")
        return None

    print(f"Found {len(sac_files)} .sac files")

    all_data = []
    for i, filename in enumerate(sac_files, 1):
        try:
            print(f"Loading file {i}/{len(sac_files)}: {filename}")
            st = read(filename)
            tr = st[0]  # Get the first trace
            all_data.append(tr.data)
            print(f"  Shape: {tr.data.shape}, dtype: {tr.data.dtype}")
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue

    if not all_data:
        print("No data was successfully loaded")
        return None

    # Concatenate all data arrays
    concatenated_data = np.concatenate(all_data)
    print(f"\nConcatenation complete!")
    print(f"Final array shape: {concatenated_data.shape}")
    print(f"Final array dtype: {concatenated_data.dtype}")

    return concatenated_data

def main():
    url = "https://zenodo.org/records/10457508/files/data.tar.gz?download=1"
    local_file = "lim_et_al_2024.zip"
    sac_directory = "data/01"
    output_file = "lim_et_al_2024.01.concat.npy"

    # Download if needed
    if not download_file(url, local_file):
        print("Failed to download file")
        sys.exit(1)

    # Extract data folder
    if not extract_data_folder(local_file):
        print("Failed to extract data folder")
        sys.exit(1)

    # Load and concatenate SAC files
    concatenated_data = load_and_concatenate_sac_files(sac_directory)
    if concatenated_data is None:
        print("Failed to process SAC files")
        sys.exit(1)

    # Save concatenated data
    print(f"\nSaving concatenated data to {output_file}...")
    try:
        np.save(output_file, concatenated_data)
        print("Data saved successfully")
    except Exception as e:
        print(f"Error saving data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
