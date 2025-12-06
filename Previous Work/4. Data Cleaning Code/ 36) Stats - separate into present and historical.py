import os
import pandas as pd

def split_current_historical():
    folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(folder, "Stats - QBDataCube.csv")

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Load CSV
    df = pd.read_csv(file_path)

    # Identify players with an entry in 2026
    current_players = df[df['YEAR'] == 2026]['PLAYER NAME'].unique()
    print(f"Found {len(current_players)} current players (2026).")

    # Current players: all rows for these players
    df_current = df[df['PLAYER NAME'].isin(current_players)]
    # Historical players: all rows for players NOT in current_players
    df_historical = df[~df['PLAYER NAME'].isin(current_players)]

    # Save CSVs
    current_path = os.path.join(folder, "Stats - QBDataCube_current.csv")
    historical_path = os.path.join(folder, "Stats - QBDataCube_historical.csv")

    df_current.to_csv(current_path, index=False)
    df_historical.to_csv(historical_path, index=False)

    print(f"Saved current players to {current_path}")
    print(f"Saved historical players to {historical_path}")

if __name__ == "__main__":
    split_current_historical()
