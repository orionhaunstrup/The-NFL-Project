import os
import pandas as pd

# Columns to remove if they start with any of these strings
REMOVE_PREFIXES = ["1st downs", "1st down %", "20+", "40+"]

folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if not filename.endswith(".csv"):
        continue

    file_path = os.path.join(folder, filename)
    df = pd.read_csv(file_path)

    # Identify columns to drop
    to_drop = [col for col in df.columns if any(col.startswith(prefix) for prefix in REMOVE_PREFIXES)]

    if to_drop:
        df.drop(columns=to_drop, inplace=True)
        print(f"{filename}: Dropped columns → {to_drop}")
        # Save cleaned file (overwrite)
        df.to_csv(file_path, index=False)
    else:
        print(f"{filename}: No columns to drop")
