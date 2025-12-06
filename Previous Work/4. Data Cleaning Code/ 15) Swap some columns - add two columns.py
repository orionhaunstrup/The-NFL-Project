import os
import pandas as pd

folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if not filename.endswith(".csv"):
        continue

    file_path = os.path.join(folder, filename)
    df = pd.read_csv(file_path)

    # Ensure 12th column is "20+"
    if len(df.columns) < 12 or df.columns[11] != "20+":
        df.insert(11, "20+", ["*"] * len(df))
        print(f"{filename}: Inserted 12th column '20+' filled with '*'")
    else:
        print(f"{filename}: 12th column already '20+'")

    # Ensure 13th column is "40+"
    if len(df.columns) < 13 or df.columns[12] != "40+":
        df.insert(12, "40+", ["*"] * len(df))
        print(f"{filename}: Inserted 13th column '40+' filled with '*'")
    else:
        print(f"{filename}: 13th column already '40+'")

    # Save updated CSV (overwrite)
    df.to_csv(file_path, index=False)
