import os
import pandas as pd

def condense_player_data_to_list(file_name):
    folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(folder, file_name)

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    df = pd.read_csv(file_path)

    # Remove YEAR column if it exists
    if 'YEAR' in df.columns:
        df.drop(columns=['YEAR'], inplace=True)

    condensed_rows = []
    for player, group in df.groupby('PLAYER NAME'):
        # Flatten all values (exclude PLAYER NAME) and convert to string
        values = group.drop(columns=['PLAYER NAME']).to_numpy().flatten()
        values_str = ",".join(map(str, values))
        condensed_rows.append([player, values_str])

    # Create new DataFrame with two columns
    condensed_df = pd.DataFrame(condensed_rows, columns=['PLAYER NAME', 'STATS'])

    # Save back to CSV
    output_path = os.path.join(folder, f"Condensed_{file_name}")
    condensed_df.to_csv(output_path, index=False)
    print(f"Condensed player data saved to {output_path}")

if __name__ == "__main__":
    for fname in ["HowGood - QBDataCube_current.csv", "HowGood - QBDataCube_historical.csv"]:
        condense_player_data_to_list(fname)
