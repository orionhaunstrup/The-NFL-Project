import os
import pandas as pd

# Folder where the script is located
folder = os.path.dirname(os.path.abspath(__file__))

print(f"Looking in folder: {folder}")

csv_found = False

for filename in os.listdir(folder):
    if filename.endswith(".csv"):
        csv_found = True
        file_path = os.path.join(folder, filename)
        print(f"Processing {filename}...")

        # Read CSV
        df = pd.read_csv(file_path)

        # Title-case all column headers
        df.columns = [col.title() for col in df.columns]

        # Ensure first column is "Player Name"
        if len(df.columns) > 0:
            df.columns.values[0] = "Player Name"

        # Save back to the same file
        df.to_csv(file_path, index=False)
        print(f"Updated column titles in {filename}")

if not csv_found:
    print("No CSV files found in this folder.")
