import os
import csv

def load_positions(filename=" 0) player_positions.txt"):
    positions = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Split on " - " (space-dash-space)
            if " - " in line:
                name, pos = line.split(" - ", 1)
                positions[name.strip()] = pos.strip()
            else:
                print(f"WARNING: Could not parse line in positions file: {line}")

    return positions


def prune_rushing_files():
    positions = load_positions()

    for file in os.listdir("."):
        if not file.startswith("NFL_Passing_") or not file.endswith(".csv"):
            continue

        print(f"Processing {file}...")

        with open(file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        if not rows:
            print(f"{file} is empty, skipping.")
            continue

        header = rows[0]
        data_rows = rows[1:]

        pruned_rows = []

        for row in data_rows:
            if not row:
                continue

            player = row[0].strip()

            # Look up position
            position = positions.get(player)

            # Keep QBs or unknowns
            if position == "QB" or position is None:
                pruned_rows.append(row)
            # else:
            #     print(f"  Removing: {player} ({position})")

        # Output filename
        outname = file.replace(".csv", "_PRUNED.csv")

        with open(outname, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(pruned_rows)

        print(f"  → Wrote pruned data to {outname}")


if __name__ == "__main__":
    prune_rushing_files()
