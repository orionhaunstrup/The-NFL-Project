import os
import pandas as pd

def add_total_column():
    folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(folder, "HowGood - QBDataCube.csv")

    if not os.path.exists(file_path):
        print(f"QBDataCube.csv not found in {folder}")
        return

    df = pd.read_csv(file_path)

    # Identify columns to sum: everything except first two columns (PLAYER NAME and YEAR)
    sum_cols = df.columns[2:]

    # Add TOTAL column
    df["TOTAL"] = df[sum_cols].apply(pd.to_numeric, errors='coerce').sum(axis=1)

    # Save back to CSV
    df.to_csv(file_path, index=False)
    print(f"TOTAL column added and saved in {file_path}")

if __name__ == "__main__":
    add_total_column()
