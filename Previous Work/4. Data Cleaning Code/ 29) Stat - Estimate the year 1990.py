import pandas as pd
from tqdm import tqdm  # pip install tqdm if you don't have it

def repair_1990_stats():
    file_path = "Stats - QBDataCube.csv"
    df = pd.read_csv(file_path)

    # Convert columns 11, 12, 25, 26, 27 (1-indexed) to 0-indexed
    corrupted_cols = [10, 11, 24, 25, 26]

    # Columns to construct vectors: exclude PLAYER NAME (0), YEAR (1), and corrupted_cols
    vector_cols = [i for i in range(df.shape[1]) if i not in [0, 1] + corrupted_cols]

    # Separate 1990 rows
    df_1990 = df[df['YEAR'] == 1990]
    df_rest = df[(df['YEAR'] != 1990) & (df['YEAR'] >= 1981) & (df['YEAR'] <= 2024)]

    print(f"Repairing {len(df_1990)} rows for 1990...")

    # Loop over 1990 rows with a progress bar
    for idx_1990, row_1990 in tqdm(df_1990.iterrows(), total=len(df_1990), desc="Processing 1990 rows"):
        vec_1990 = row_1990.iloc[vector_cols].apply(pd.to_numeric, errors='coerce').fillna(0).values

        min_dist = float('inf')
        best_match = None

        for idx_other, row_other in df_rest.iterrows():
            vec_other = row_other.iloc[vector_cols].apply(pd.to_numeric, errors='coerce').fillna(0).values
            dist = ((vec_1990 - vec_other)**2).sum()
            if dist < min_dist:
                min_dist = dist
                best_match = row_other

        # Copy the corrupted columns from the best match
        for col_idx in corrupted_cols:
            df.at[idx_1990, df.columns[col_idx]] = best_match.iloc[col_idx]

    # Save repaired CSV
    df.to_csv(file_path, index=False)
    print("Repaired corrupted 1990 stats in Stats - QBDataCube.csv")

if __name__ == "__main__":
    repair_1990_stats()
