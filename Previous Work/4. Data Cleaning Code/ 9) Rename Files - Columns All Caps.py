import os
import pandas as pd

folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if not filename.endswith(".csv"):
        continue

    file_path = os.path.join(folder, filename)
    df = pd.read_csv(file_path)

    # Convert all column titles to uppercase
    df.columns = [col.upper() for col in df.columns]

    # Save updated CSV (overwrite)
    df.to_csv(file_path, index=False)
    print(f"{filename}: Converted column titles to uppercase")
