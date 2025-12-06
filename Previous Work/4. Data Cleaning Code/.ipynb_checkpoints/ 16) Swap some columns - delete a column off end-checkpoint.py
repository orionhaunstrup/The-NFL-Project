import os
import pandas as pd

folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if not filename.endswith(".csv"):
        continue

    file_path = os.path.join(folder, filename)
    df = pd.read_csv(file_path)

    # Keep only the first 16 columns
    if len(df.columns) > 16:
        df = df.iloc[:, :16]
        print(f"{filename}: Deleted columns after 16th")
    else:
        print(f"{filename}: 16 or fewer columns, nothing to delete")

    # Save updated CSV (overwrite)
    df.to_csv(file_path, index=False)
