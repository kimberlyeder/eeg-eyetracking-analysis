# EDF File Conversion Instructions

## Problem
Your eye-tracking data is in EyeLink EDF (proprietary binary) format, which requires SR Research tools to convert.

## Solution: Convert EDF to ASC Format

### Step 1: Download SR Research EDF2ASC Converter

1. Go to: https://www.sr-research.com/support/thread-13.html
2. Download **EyeLink Developers Kit** for Windows
3. Install the software (you only need the edf2asc.exe utility)

### Step 2: Convert Your Files

Open PowerShell in your project directory and run:

```powershell
cd Data
edf2asc -t -s -miss -1.0 -y *.EDF
```

**Command explanation:**
- `-t`: Include time stamps
- `-s`: Include samples (gaze data)
- `-miss -1.0`: Use -1.0 for missing data
- `-y`: Overwrite existing files
- `*.EDF`: Convert all EDF files

### Step 3: Verify Conversion

After conversion, you should see .asc files:
```powershell
ls *.asc
```

You should see:
- `201101_2025_11_20_13_16.asc`
- `201102_2025_11_20_15_02.asc`
- `201105_2025_11_20_16_25.asc`
- `tb171106_2025_11_17_11_36.asc`

### Step 4: Re-run Notebook

Once ASC files exist, re-run the notebook cells. The parsing function will automatically detect and use ASC files.

## Alternative: Manual Export

If you can't install edf2asc:

1. Install **EyeLink Data Viewer** (free from SR Research)
2. Open each EDF file
3. Export as ASCII format
4. Save in the Data/ directory with .asc extension

## Your Files

Found 4 EDF files to convert:
1. `201101_2025_11_20_13_16.EDF` → Session 1
2. `201102_2025_11_20_15_02.EDF` → (no match)
3. `201105_2025_11_20_16_25.EDF` → (no match)
4. `tb171106_2025_11_17_11_36.EDF` → Session 0

Note: Session 4 has no matching EDF file.
