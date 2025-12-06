import os
import pandas as pd

folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if not filename.endswith(".csv"):
        continue

    file_path = os.path.join(folder, filename)
    df = pd.read_csv(file_path)

    # Swap 5th and 6th columns (indexes 4 and 5)
    if len(df.columns) >= 6:
        cols = df.columns.tolist()
        cols[4], cols[5] = cols[5], cols[4]
        df = df[cols]
        print(f"{filename}: Swapped columns 5 and 6")
    else:
        print(f"{filename}: Not enough columns to swap 5 and 6")

    # Save updated CSV (overwrite)
    df.to_csv(file_path, index=False)
