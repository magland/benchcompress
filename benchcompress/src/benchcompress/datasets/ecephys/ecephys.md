# Extracellular Electrophysiology Dataset

Extracellular Electrophysiology datasets contain recordings of electrical activity from neurons in the brain. These recordings are made using microelectrodes that detect the small voltage changes produced by neurons when they fire action potentials (spikes).

## Data Sources

The datasets are samples from single channels within larger electrophysiology recordings available on the DANDI Archive:

- Channel 45 from a session in [Dandiset 000876](https://dandiarchive.org/dandiset/000876)
- Channel 101 from a session in [Dandiset 000409](https://dandiarchive.org/dandiset/000409)
- Channel 0 from a session in [Dandiset 001290](https://dandiarchive.org/dandiset/001290)
- Only channel from a session in [Dandiset 001259](https://dandiarchive.org/dandiset/001259)

## Dataset Variants

We provide three types of variants for each sampled channel:

### 1. Raw Data
- Direct recordings from the electrodes
- Contains both neural signals and background noise
- Integer-valued samples representing voltage
- Sampling rate: 30 kHz

### 2. Filtered Data
- Bandpass filtered between 300-6000 Hz to isolate spike activity
- Normalized by estimated noise level
- Quantized with step size 0.25
- Stored as 16-bit integers

### 3. Sparse Data
- Applies activity-based suppression to focus on regions with neural firing
- Uses adaptive thresholding to detect active regions
- Suppresses low-activity regions while preserving spike waveforms
- Also quantized and stored as 16-bit integers

## Compression Considerations

These datasets present different challenges for compression algorithms:

1. Raw data contains broadband noise and slow drifts
2. Filtered data emphasizes spike waveforms but maintains continuous values
3. Sparse data has many near-zero regions interspersed with spike events

The sparse variants are particularly interesting as they represent a common preprocessing step in neuroscience analysis, where only time periods containing neural activity are retained.
