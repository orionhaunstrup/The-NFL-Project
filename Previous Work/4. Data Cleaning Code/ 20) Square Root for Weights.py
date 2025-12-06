import os
import pandas as pd
import numpy as np

# Folder containing the CSV files
folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if not filename.endswith(".csv"):
        continue

    file_path = os.path.join(folder, filename)
    df = pd.read_csv(file_path)

    def transform(x):
        if str(x).strip() == "*":
            return x
        try:
            val = float(x)
            if val <= 0:
                return 0
            else:
                return np.sqrt(val)
        except:
            return x  # leave non-numeric as-is

    df = df.applymap(transform)
    print(f"Processed {filename}")

    df.to_csv(file_path, index=False)
