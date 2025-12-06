import os
import pandas as pd

def prune_pre1981_players():
    folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(folder, "Stats - QBDataCube.csv")

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Load CSV
    df = pd.read_csv(file_path)

    # Find all players with a YEAR <= 1980
    players_to_remove = df[df['YEAR'] <= 1980]['PLAYER NAME'].unique()
    print(f"Found {len(players_to_remove)} players with first entry in 1980 or earlier. Removing them...")

    # Keep only rows for players not in that list
    df_pruned = df[~df['PLAYER NAME'].isin(players_to_remove)]

    # Save pruned CSV (overwrite)
    df_pruned.to_csv(file_path, index=False)
    print(f"Pruned Stats - QBDataCube.csv. Removed all years for {len(players_to_remove)} players.")

if __name__ == "__main__":
    prune_pre1981_players()
