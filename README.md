# EEG Analysis Pipeline for Human-LLM Alignment Study

This repository contains the complete EEG preprocessing and ERP analysis pipeline for studying neural responses to AI-generated text with varying alignment levels.

## Overview

The study investigates how the brain processes AI-generated responses with different levels of alignment (high/medium/low) to human responses. EEG data is recorded while participants read AI text, and Event-Related Potentials (ERPs) are analyzed to identify neural markers of alignment perception.

## Pipeline Structure

The analysis pipeline consists of sequential Jupyter notebooks:

### 1. Session Mapping
- **`01_Map_Sessions.ipynb`**: Matches experiment CSV files with EEG recordings based on Unix timestamps

### 2. EEG Preprocessing
- **`02_EEG_Preprocess-RAW.ipynb`**: Loads raw EEG data from CSV files
- **`03_EEG_Preprocess-RANSAC.ipynb`**: Identifies and removes bad channels using RANSAC
- **`04_EEG_Preprocess-ICA.ipynb`**: Applies ICA with ICLabel for artifact removal

### 3. ERP Analysis
- **`05_ERP_Analysis.ipynb`**: Single-session ERP analysis including:
  - Event extraction from experiment data
  - Epoch creation and artifact rejection (AutoReject)
  - ERP averaging and visualization
  - Component identification (N1, P2, N2, P300, N400, LPP, Late Negativity)
  - Statistical quality assessment
- **`06_Grand_Average_ERP.ipynb`**: Multi-session grand average analysis:
  - Combines epochs from all sessions (N=3 participants)
  - Computes grand average ERPs by condition
  - Generates publication-quality waveforms and topomaps
  - Extracts mean amplitudes for component time windows
  - Exports amplitude data and condition comparisons

### 4. Eye Tracking (Supplementary)
- **`07_EyeEvents.ipynb`**: Eye-tracking event parsing and feature extraction
- **`08_Eye_plotting.ipynb`**: Eye-tracking visualization
- **`09_Eye_Stats_Python.ipynb`**: Linear mixed-effects models for eye-tracking data:
  - Tests effects of alignment condition on pupil size, fixation duration, saccade metrics
  - Uses `statsmodels.MixedLM` for LME modeling
  - Generates boxplots and statistical summaries
  - Exports model comparisons (AIC/BIC) and descriptive statistics

### 5. VAS Rating (Supplementary)
- **`10_VAS_Rating_Results.ipynb`**: VAS Rating Analysis

## Preprocessing Details

### Filtering
- **Bandpass**: 1-20 Hz (removes DC drift and muscle artifacts)
- **Notch**: 50 Hz (removes line noise)
- **ICA filter**: 1-100 Hz (temporary, for ICLabel compatibility)

### Artifact Removal
- **Bad channels**: RANSAC algorithm (removed: F7, P9, F3)
- **ICA components**: ICLabel classification (excludes non-brain components)
- **Epoch rejection**: AutoReject with adaptive cross-validation
- **Amplitude threshold**: 100-150 µV peak-to-peak fallback

### Epoching
- **Time window**: -0.5 to 0.8 seconds
- **Baseline**: -0.5 to -0.1 seconds
- **Event marker**: `AI_Response.started` (when AI text is displayed)

## Data Structure

```
Data/                                    # Raw experiment and EEG data (not in repo)
├── 01_human-llm-alignment_*.csv        # Experiment behavior data
└── EEG_data_*.csv                      # Raw EEG recordings

preprocessed/                            # Intermediate processing files (not in repo)
├── session_XX-EEG-raw.pkl              # Raw EEG arrays
├── session_XX-EEG-preprocessed.pkl     # After ICA artifact removal
├── X-epochs-epo.fif                    # Epoched data (per session)
├── X-evoked-*.fif                      # Condition-averaged ERPs (per session)
└── eye_tracking_features.csv           # Eye-tracking metrics by trial

figures/                                 # Generated plots (not in repo)
├── erp_*.png                           # ERP waveforms and topomaps
├── grand_average_*.png                 # Grand average visualizations
└── eye_stats_*.png                     # Eye-tracking statistical plots

results/                                 # Analysis outputs (not in repo)
├── *_amplitudes.csv                    # ERP amplitude extractions
├── grand_average_*.csv                 # Grand average summaries
└── eye_stats_*.csv                     # Eye-tracking statistical results

session_mapping.csv                      # Session metadata (included in repo)
```

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Analyse
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run notebooks in sequence:

1. Place raw data in `Data/` folder
2. Run `01_Map_Sessions.ipynb` to create session mapping
3. Run preprocessing notebooks (02-04) in order for each session
4. Run `05_ERP_Analysis.ipynb` for each session to generate epochs
5. Run `06_Grand_Average_ERP.ipynb` to combine sessions and compute grand averages
6. (Optional) Run eye-tracking notebooks (07, 08, 09) for supplementary analysis

Each notebook includes detailed documentation and quality checks.

## Key Features

- **Automatic session matching**: Timestamps-based alignment of experiment and EEG data
- **Robust artifact removal**: Multi-stage pipeline (RANSAC + ICA + AutoReject)
- **Quality assessment**: Automated checks for epoch count, amplitude, SNR
- **Adaptive processing**: Handles edge cases (few epochs, high noise)
- **Comprehensive diagnostics**: Drop logs, rejection summaries, component identification

## Requirements

- Python 3.8+
- MNE-Python 1.5+ (EEG/MEG analysis)
- AutoReject (artifact detection)
- MNE-ICALabel (ICA component classification)
- statsmodels (linear mixed-effects models)
- Standard scientific Python stack (NumPy, Pandas, Matplotlib, Seaborn, SciPy)

See `requirements.txt` for complete list.

## Experimental Design

- **Participants**: N=3 (Sessions 0, 1, 4)
- **Conditions**: 3 alignment levels (high, medium, low)
- **Stimuli**: AI-generated text responses to social scenarios
- **Task**: Read AI responses after providing own response
- **EEG**: 64-channel system, 500 Hz sampling rate
- **Eye-tracking**: EyeLink system, synchronized with EEG
- **Expected trials**: ~50 per session (minimum 15-20 per condition for valid ERPs)
- **ERP Components**: N1, P2, N2, P300, N400, LPP, Late Negativity (500-700ms)
- **Eye Metrics**: Pupil size, fixation duration, saccade amplitude/count, ROI coverage

## Citation

If you use this pipeline, please cite:
```
Eder, K. (2025). EEG Analysis Pipeline for Human-LLM Alignment Study. 
GitHub repository: https://github.com/kimberlyeder/eeg-eyetracking-data-analysis
```

## License

MIT License

## Contact

Kimberly Eder
- GitHub: [@kimberlyeder](https://github.com/kimberlyeder)
- Repository: [eeg-eyetracking-analysis](https://github.com/kimberlyeder/eeg-eyetracking-analysis)
