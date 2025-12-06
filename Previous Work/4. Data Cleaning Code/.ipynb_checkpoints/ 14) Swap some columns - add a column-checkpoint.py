import os
import pandas as pd

folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if not filename.endswith(".csv"):
        continue

    file_path = os.path.join(folder, filename)
    df = pd.read_csv(file_path)

    # Insert 9th column (index 8) as "RUSHING 1ST DOWNS" filled with "*"
    if len(df.columns) < 9 or df.columns[8].upper() != "RUSHING 1ST DOWNS":
        df.insert(8, "RUSHING 1ST DOWNS", ["*"] * len(df))
        print(f"{filename}: Inserted 9th column 'RUSHING 1ST DOWNS' filled with '*'")
    else:
        print(f"{filename}: 9th column already 'RUSHING 1ST DOWNS'")

    # Insert 10th column (index 9) as "RUSHING 1ST %" filled with "*"
    if len(df.columns) < 10 or df.columns[9].upper() != "RUSHING 1ST %":
        df.insert(9, "RUSHING 1ST %", ["*"] * len(df))
        print(f"{filename}: Inserted 10th column 'RUSHING 1ST %' filled with '*'")
    else:
        print(f"{filename}: 10th column already 'RUSHING 1ST %'")

    # Insert 11th column (index 10) as "FUMBLES" filled with "*"
    if len(df.columns) < 11 or df.columns[10].upper() != "FUMBLES":
        df.insert(10, "FUMBLES", ["*"] * len(df))
        print(f"{filename}: Inserted 11th column 'FUMBLES' filled with '*'")
    else:
        print(f"{filename}: 11th column already 'FUMBLES'")

    # Save updated CSV (overwrite)
    df.to_csv(file_path, index=False)
