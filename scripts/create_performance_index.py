import pandas as pd
import os

# Create the preprocessed folder if it doesn't exist
os.makedirs("./preprocessed", exist_ok=True)

# Load the experiment data
df = pd.read_csv("./Data/01_human-llm-alignment_2025-11-17_16h18.55.779.csv")

# Filter only rows with actual trials (not the header row)
df = df[df['task.started_Unix'].notna()].copy()

# Create the performance-index.csv
performance_data = []

for idx, row in df.iterrows():
    performance_data.append({
        'pid': 1,  # Your participant ID
        'TimeStart': row['task.started_Unix'] * 1000,  # Convert to milliseconds
        'TimeEnd': row['task.stopped_Unix'] * 1000,     # Convert to milliseconds
        'Condition': row['Alignment'] if pd.notna(row['Alignment']) else 'unknown',  # high/low alignment
        'TaskCount': idx + 1,
        'IsCorrect': True  # Adjust based on your data if available
    })

# Create DataFrame and save as CSV
df_performance = pd.DataFrame(performance_data)
df_performance.to_csv("./preprocessed/performance-index.csv", index=False)

print(f"Performance index created with {len(df_performance)} entries")
print(df_performance.head())
