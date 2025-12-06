import os
import pandas as pd

def keep_only_total_columns():
    folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(folder, "HowGood - QBDataCube.csv")

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    df = pd.read_csv(file_path)

    # Columns to keep
    keep_cols = ["PLAYER NAME", "YEAR", "TOTAL"]

    # Filter dataframe to only keep the desired columns
    existing_keep_cols = [col for col in keep_cols if col in df.columns]
    df = df[existing_keep_cols]

    # Save back to CSV
    df.to_csv(file_path, index=False)
    print(f"Filtered HowGood - QBDataCube.csv to keep only: {existing_keep_cols}")

if __name__ == "__main__":
    keep_only_total_columns()
