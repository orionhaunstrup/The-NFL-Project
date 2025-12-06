import os
import pandas as pd
import re

# Folder where this .py file is located
folder = os.path.dirname(os.path.abspath(__file__))
print(f"Looking in folder: {folder}")

csv_files = [f for f in os.listdir(folder) if f.startswith("NFL_Rushing_") and f.lower().endswith(".csv")]

if not csv_files:
    print("No matching CSV files found.")
else:
    for filename in csv_files:
        # Extract year from filename
        m = re.search(r"(\d{4})", filename)
        year = m.group(1) if m else "Unknown"
        print(f"Processing {filename} (Year: {year})...")

        file_path = os.path.join(folder, filename)
        df = pd.read_csv(file_path)

        # Fill blanks and NaN with '*'
        df = df.fillna('*')
        for col in df.columns:
            df[col] = df[col].replace('', '*')

        # Save back
        df.to_csv(file_path, index=False)
        print(f"  → Finished {filename}")

print("All CSV files processed.")
