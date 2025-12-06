import csv
from collections import defaultdict
from pathlib import Path

INPUT = Path("Stats - QBDataCube.csv")
OUTPUT = Path("Stats - QBDataCube_blended.csv")

# --------------------------------------------------------------
# Load original cube
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
# Identify PLAYER NAME columns (case-insensitive)
# --------------------------------------------------------------
player_name_cols = [i for i, col in enumerate(header) if col.strip().upper() == "PLAYER NAME"]

# Identify numeric columns (all except PLAYER NAME and YEAR)
numeric_cols = [i for i in range(len(header)) if i not in player_name_cols + [1]]  # column 1 is YEAR

# --------------------------------------------------------------
# Group rows by player
# --------------------------------------------------------------
players = defaultdict(list)
for row in rows:
    name = row[0].strip()
    year = int(row[1])
    players[name].append((year, row))

# --------------------------------------------------------------
# Build blended cube
# --------------------------------------------------------------
blended_rows = []

for player, year_row_list in players.items():
    # Sort by year
    year_row_list.sort(key=lambda x: x[0])
    
    # Map year -> full row for numeric extraction
    year_to_row = {year: row for year, row in year_row_list}
    
    # Determine extended year range (2 before first, 2 after last)
    first_year = year_row_list[0][0]
    last_year = year_row_list[-1][0]
    extended_years = range(first_year - 2, last_year + 3)  # inclusive of 2 after

    for year in extended_years:
        new_row = []

        for col_idx in range(len(header)):
            if col_idx == 0:
                new_row.append(player)  # main PLAYER NAME
            elif col_idx == 1:
                new_row.append(year)  # YEAR
            elif col_idx in player_name_cols:
                new_row.append(player)  # repeat PLAYER NAME
            else:  # numeric columns
                # Sum over 5-year window: year-2, year-1, year, year+1, year+2
                total = 0
                for offset in range(-2, 3):
                    y = year + offset
                    if y in year_to_row:
                        try:
                            total += float(year_to_row[y][col_idx])
                        except:
                            total += 0  # in case of non-numeric
                    # missing year treated as 0
                blended_value = total / 5
                new_row.append(blended_value)

        blended_rows.append(new_row)

# --------------------------------------------------------------
# Sort final blended cube by PLAYER NAME → YEAR
# --------------------------------------------------------------
blended_rows.sort(key=lambda r: (r[0].strip().lower(), int(r[1])))

# --------------------------------------------------------------
# Write blended cube to CSV
# --------------------------------------------------------------
with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(blended_rows)

print(f"Blended QBDataCube created: {OUTPUT}")
print(f"Total rows in blended cube: {len(blended_rows)}")
