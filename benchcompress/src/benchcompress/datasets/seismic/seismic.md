# Seismic Dataset

This dataset contains marine seismic reflection data. Processed seismic reflection data and associated files from Roger Revelle voyage RR1508: 16 May - 18 June 2015. The research voyage aimed to characterise the thermal regime of the gas hydrate systems on the southern Hikurangi margin east of New Zealand. Data were processed using the Globe Claritas processing software.

## Data Source

The data comes from a SEG-Y file available on Zenodo (https://zenodo.org/records/8152964). SEG-Y is a standard format for storing seismic data that includes both the recorded waveforms and metadata about the survey.

## Variants

We provide two versions of the seismic data:

### 1. Raw Data (seismic-04A-04B)
- Original floating point values from the SEG-Y file
- Contains the natural amplitude variations of the seismic waves
- Stored as 32-bit floating point numbers

### 2. Quantized Data (seismic-04A-04B-quantized)
- Values are scaled and rounded to integers
- Uses a quantization step of 10000
- Stored as 32-bit integers
