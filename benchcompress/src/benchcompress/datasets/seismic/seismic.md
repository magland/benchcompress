# Seismic Dataset

This dataset contains marine seismic reflection data. Processed seismic reflection data and associated files from Roger Revelle voyage RR1508: 16 May - 18 June 2015. The research voyage aimed to characterise the thermal regime of the gas hydrate systems on the southern Hikurangi margin east of New Zealand. Data were processed using the Globe Claritas processing software.

## Data Source

The data comes from a SEG-Y file available on Zenodo (https://zenodo.org/records/8152964). SEG-Y is a standard format for storing seismic data that includes both the recorded waveforms and metadata about the survey.

## Variants

We provide two datasets with two versions each:

### Revelle RR1508 Data (seismic-04A-04B)
- Original floating point values from the SEG-Y file
- Contains the natural amplitude variations of the seismic waves
- Stored as 32-bit floating point numbers

### Revelle RR1508 Quantized Data (seismic-04A-04B-quantized)
- Values are scaled and rounded to integers
- Uses a quantization step of 10000
- Stored as 32-bit integers

### Goesan Earthquake Data (seismic-lim-2024-01)
- Original floating point values from the continuous seismic recording
- Data from the 2022 Mw 3.8 earthquake in Goesan, South Korea
- Part of a study analyzing 42 earthquakes including foreshocks and aftershocks
- Records from permanent seismic networks with closest station at 8.3 km from epicenter
- Stored as 32-bit floating point numbers

### Goesan Earthquake Quantized Data (seismic-lim-2024-01-quantized)
- Values are scaled and rounded to integers
- Uses a quantization step of 10000
- Stored as 32-bit integers

## Source Details

### Roger Revelle RR1508
The data comes from a SEG-Y file available on Zenodo (https://zenodo.org/records/8152964). SEG-Y is a standard format for storing seismic data that includes both the recorded waveforms and metadata about the survey.

### Goesan Earthquake 2022
This dataset contains seismic recordings from the 2022 Mw 3.8 Goesan earthquake in South Korea. The earthquake occurred on October 28, 2022, and was preceded by a Mw 3.3 foreshock 17 seconds before the mainshock. The study analyzed 42 earthquakes in total, including the mainshock, foreshock, and aftershocks, to understand the interactions between seismic events. The data revealed that the mainshock occurred at the southeastern tip of the hypocenter distribution of three foreshocks, with aftershocks showing a diffused pattern propagating toward both ends of the inferred lineament. The data is available on Zenodo (https://zenodo.org/records/14774624).
