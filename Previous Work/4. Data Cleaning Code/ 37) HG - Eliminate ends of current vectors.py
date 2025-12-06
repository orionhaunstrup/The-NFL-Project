import os
import pandas as pd
import ast

def prune_receiving_lists(file_name):
    folder = os.getcwd()
    file_path = os.path.join(folder, file_name)

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    df = pd.read_csv(file_path)

    # Container for pruned rows
    pruned_rows = []

    for i, row in df.iterrows():
        player = row['PLAYER NAME']
        stats_str = row['STATS']

        try:
            # Convert string back to list of floats
            stats_list = ast.literal_eval(f"[{stats_str}]")
        except Exception as e:
            print(f"Skipping {player} due to parse error: {e}")
            continue

        if len(stats_list) <= 4:
            # Skip this row entirely
            continue

        # Trim last 4 elements
        trimmed_list = stats_list[:-4]

        # Convert back to string
        trimmed_str = ",".join(map(str, trimmed_list))

        pruned_rows.append([player, trimmed_str])

    # Create new DataFrame
    pruned_df = pd.DataFrame(pruned_rows, columns=['PLAYER NAME', 'STATS'])

    # Save back (overwrite)
    pruned_df.to_csv(file_path, index=False)
    print(f"Pruned {file_name}: kept {len(pruned_df)} rows after trimming last 4 elements.")

if __name__ == "__main__":
    prune_receiving_lists("HowGood_ReceivingDataCube_current.csv")
