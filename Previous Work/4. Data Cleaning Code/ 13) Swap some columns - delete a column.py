import os
import pandas as pd

folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if not filename.endswith(".csv"):
        continue

    file_path = os.path.join(folder, filename)
    df = pd.read_csv(file_path)

    # Delete 9th column (index 8)
    if len(df.columns) >= 9:
        col_to_drop = df.columns[8]
        df.drop(columns=[col_to_drop], inplace=True)
        print(f"{filename}: Deleted 9th column → {col_to_drop}")
    else:
        print(f"{filename}: Not enough columns to delete 9th column")

    # Save updated CSV (overwrite)
    df.to_csv(file_path, index=False)
