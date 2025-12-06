import os
import pandas as pd

def replace_stars_with_zero():
    folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(folder, "Stats - QBDataCube.csv")

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Load CSV
    df = pd.read_csv(file_path)

    # Replace all "*" with 0
    df.replace("*", 0, inplace=True)

    # Optionally, convert all numeric columns to float
    for col in df.columns[2:]:  # skip PLAYER NAME and YEAR
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Save cleaned CSV
    df.to_csv(file_path, index=False)
    print(f"All '*' symbols replaced with 0 in {file_path}")

if __name__ == "__main__":
    replace_stars_with_zero()
