import csv
from collections import defaultdict
from pathlib import Path

INPUT = Path("QBDataCube.csv")
OUTPUT = Path("QBDataCube_final.csv")  # new output file

MAX_GAP_YEARS = 10  # ignore any gap longer than this

# --------------------------------------------------------------
# Load all rows, preserving header
# --------------------------------------------------------------
rows = []
with INPUT.open("r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if not row:
            continue
        rows.append(row)

# --------------------------------------------------------------
# Sort rows by PLAYER NAME (col 0), then YEAR (col 1)
# --------------------------------------------------------------
rows.sort(key=lambda r: (r[0].strip().lower(), int(r[1])))

# --------------------------------------------------------------
# Identify columns that are titled "PLAYER NAME" (case-insensitive)
# --------------------------------------------------------------
player_name_cols = [i for i, col in enumerate(header) if col.strip().upper() == "PLAYER NAME"]

# --------------------------------------------------------------
# Group rows by player
# --------------------------------------------------------------
players = defaultdict(list)
for row in rows:
    name = row[0].strip()
    year = int(row[1])
    players[name].append((year, row))

# --------------------------------------------------------------
# Build new row set with gap years inserted
# --------------------------------------------------------------
final_rows = []
gap_counts = defaultdict(int)

for player, year_row_list in players.items():
    # Sort each player's rows by year
    year_row_list.sort(key=lambda x: x[0])

    for i, (year, row) in enumerate(year_row_list):
        final_rows.append(row)  # add the actual row

        # Look ahead to next actual year
        if i < len(year_row_list) - 1:
            next_year = year_row_list[i + 1][0]
            gap_size = next_year - year - 1

            # Only insert gap rows if gap is ≤ MAX_GAP_YEARS
            if 1 <= gap_size <= MAX_GAP_YEARS:
                for missing_year in range(year + 1, next_year):
                    # Build a filler row
                    filler_row = []
                    for col_idx in range(len(header)):
                        if col_idx == 0:
                            filler_row.append(player)  # cube PLAYER NAME
                        elif col_idx == 1:
                            filler_row.append(missing_year)  # YEAR
                        elif col_idx in player_name_cols:
                            filler_row.append(player)  # repeat PLAYER NAME
                        else:
                            filler_row.append("0")  # all other columns → 0
                    final_rows.append(filler_row)
                    gap_counts[player] += 1

# --------------------------------------------------------------
# Sort again by PLAYER NAME → YEAR to ensure order
# --------------------------------------------------------------
final_rows.sort(key=lambda r: (r[0].strip().lower(), int(r[1])))

# --------------------------------------------------------------
# Write final sorted cube with gap-year rows
# --------------------------------------------------------------
with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(final_rows)

# --------------------------------------------------------------
# Print statistics
# --------------------------------------------------------------
total_gaps = sum(gap_counts.values())
most_gaps_player = max(gap_counts, key=lambda p: gap_counts[p]) if gap_counts else None

print(f"Final QBDataCube created: {OUTPUT}")
print(f"Added {total_gaps} gap-year rows (max gap {MAX_GAP_YEARS} years).")
if most_gaps_player:
    print(f"Player with the most gap years inserted: {most_gaps_player} ({gap_counts[most_gaps_player]} gaps)")
else:
    print("No gap years added.")
