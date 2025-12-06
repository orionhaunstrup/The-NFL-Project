import os
import pandas as pd

def prune_1938_players():
    folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(folder, "HowGood - QBDataCube_blended.csv")

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Load CSV
    df = pd.read_csv(file_path)

    # Find all players whose first entry is in 1938
    players_1938 = df[df['YEAR'] == 1938]['PLAYER NAME'].unique()
    print(f"Found {len(players_1938)} players who started in 1938. Removing them...")

    # Keep only rows for players not in that list
    df_pruned = df[~df['PLAYER NAME'].isin(players_1938)]

    # Save pruned CSV (overwrite)
    df_pruned.to_csv(file_path, index=False)
    print(f"Pruned HowGood - QBDataCube_blended.csv. Removed all years for {len(players_1938)} players.")

if __name__ == "__main__":
    prune_1938_players()
