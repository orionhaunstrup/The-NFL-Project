import os
import pandas as pd

# Folder containing the CSV files
folder = os.path.dirname(os.path.abspath(__file__))

# Column weight mapping
weights = {
    "ATTEMPTS": 0.5,
    "COMPLETION %": 2,
    "INTERCEPTIONS": -3,
    "QB RATING": 2,
    "LONG": 0.5,
    "SACKS": -1,
    "SACK LOSS YARDS": -1
}

for filename in os.listdir(folder):
    if not filename.endswith(".csv"):
        continue

    file_path = os.path.join(folder, filename)
    df = pd.read_csv(file_path)

    for col, weight in weights.items():
        if col in df.columns:
            # Apply multiplication only to numeric entries
            def multiply_if_numeric(x):
                try:
                    if str(x).strip() == "*":
                        return x
                    return float(x) * weight
                except:
                    return x  # leave non-numeric as-is

            df[col] = df[col].apply(multiply_if_numeric)
            print(f"{filename}: Applied weight {weight} to column '{col}'")
        else:
            print(f"{filename}: Column '{col}' not found, skipped")

    # Save updated CSV (overwrite)
    df.to_csv(file_path, index=False)
