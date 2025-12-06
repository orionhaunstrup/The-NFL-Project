import os
import pandas as pd

folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if not filename.endswith(".csv"):
        continue

    file_path = os.path.join(folder, filename)
    df = pd.read_csv(file_path)

    # Ensure we have at least 3 columns to calculate 2 ÷ 3
    if len(df.columns) >= 3:
        # Define a function for safe division
        def safe_divide(row):
            try:
                val2 = float(row.iloc[1])
                val3 = float(row.iloc[2])
                if val3 == 0:
                    return "*"
                return val2 / val3
            except:
                return "*"

        # Calculate the new column
        new_col = df.apply(safe_divide, axis=1)

        # Insert as 4th column (index 3)
        df.insert(3, "YARDS PER ATTEMPT", new_col)
        print(f"{filename}: Added 'YARDS PER ATTEMPT' as 4th column")
    else:
        print(f"{filename}: Not enough columns to calculate 'YARDS PER ATTEMPT'")

    # Save updated CSV (overwrite)
    df.to_csv(file_path, index=False)
