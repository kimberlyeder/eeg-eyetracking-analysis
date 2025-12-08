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
- **`05_ERP_Analysis.ipynb`**: Comprehensive ERP analysis pipeline including:
  - **Batch Processing**: Automated analysis of all 21 sessions
  - Event extraction and time synchronization
  - Epoch creation with artifact rejection (AutoReject)
  - Single-session ERP analysis and visualization
  - **Grand-Average Analysis**: Cross-session pooling for publication-quality results
  - Component identification (N1, P2, N2, P300, N400, LPP, Late Negativity)
  - Statistical quality assessment and data validation
  - Publication-ready figures and topographic maps
  - CSV exports for statistical analysis

### 4. Eye Tracking (Supplementary)
- **`06_EyeEvents.ipynb`**: Eye-tracking event parsing and feature extraction
- **`07_Eye_plotting.ipynb`**: Eye-tracking visualization
- **`08_Eye_Stats.ipynb`**: Linear mixed-effects models for eye-tracking data:
  - Tests effects of alignment condition on pupil size, fixation duration, saccade metrics
  - Uses `statsmodels.MixedLM` for LME modeling
  - Generates boxplots and statistical summaries
  - Exports model comparisons (AIC/BIC) and descriptive statistics

### 5. Behavioral Analysis (Supplementary)
- **`09_VAS_Ratings_Results.ipynb`**
- **`create_performance_index.py`**: Performance metric calculation script

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
├── session_XX-EEG-raw.pkl              # Raw EEG arrays (21 sessions: 00-20)
├── session_XX-bad-channels.pkl         # RANSAC bad channel lists
├── session_XX-EEG-preprocessed.pkl     # After ICA artifact removal (21 sessions)
├── session_XX-epochs-epo.fif           # Epoched data (per session)
├── session_XX-evoked-{condition}-ave.fif  # Condition-averaged ERPs (per session)
└── eye_tracking_features.csv           # Eye-tracking metrics by trial

figures/                                 # Generated plots (not in repo)
├── grand_avg_erp_comparison.png        # Grand-average condition comparison
├── grand_avg_topomap_{condition}.png   # Grand-average topographic maps
└── eye_stats_*.png                     # Eye-tracking statistical plots

results/                                 # Analysis outputs (not in repo)
├── batch_processing_summary.csv        # Batch processing status for all 21 sessions
├── erp_session_XX_Cz.csv              # Single-session ERP data (Cz electrode)
├── erp_peaks_session_XX.csv           # Detected peaks and latencies
├── erp_identified_session_XX.csv      # Component identifications
├── erp_quality_session_XX.csv         # Data quality metrics
├── grand_avg_erp_{condition}_Cz.csv   # Grand-average ERP data per condition
├── grand_avg_erp_summary.csv          # Grand-average summary statistics
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
2. Run `01_Map_Sessions.ipynb` to create session mapping (identifies 21 sessions)
3. Run preprocessing notebooks (02-04) in order - these have batch processing for all sessions:
   - `02_EEG_Preprocess-RAW.ipynb` - Processes all 21 sessions
   - `03_EEG_Preprocess-RANSAC.ipynb` - RANSAC for all sessions
   - `04_EEG_Preprocess-ICA.ipynb` - ICA for all sessions
4. Run `05_ERP_Analysis.ipynb`:
   - First, execute **Section 4 (Batch Processing)** to automatically process all 21 sessions
   - Then execute **Section 8 (Grand-Average)** to combine sessions
   - Optional: Use Appendix sections for manual single-session inspection
5. (Optional) Run eye-tracking notebooks (Step_12, Step_14, Step_15) for supplementary analysis

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

- **Participants**: N=21 sessions (sessions 00-20)
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
