import os
import pandas as pd

def remove_total_column():
    folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(folder, "Stats - QBDataCube.csv")

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    df = pd.read_csv(file_path)

    if "TOTAL" in df.columns:
        df.drop(columns=["TOTAL"], inplace=True)
        df.to_csv(file_path, index=False)
        print("TOTAL column removed.")
    else:
        print("No TOTAL column to remove.")

if __name__ == "__main__":
    remove_total_column()
