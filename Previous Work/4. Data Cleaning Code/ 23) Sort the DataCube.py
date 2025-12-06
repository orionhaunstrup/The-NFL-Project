import csv

INPUT = "QBDataCube.csv"
OUTPUT = "QBDataCube_sorted.csv"   # safer not to overwrite original immediately

rows = []

# ----------------------------
# Load everything
# ----------------------------
with open(INPUT, "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)         # keep header exactly
    for row in reader:
        if not row:
            continue
        rows.append(row)

# ----------------------------
# Sort by: PLAYER NAME (col 0), then YEAR (col 1)
# YEAR must be converted to int
# ----------------------------
rows.sort(key=lambda r: (r[0].strip().lower(), int(r[1])))

# ----------------------------
# Save the sorted file
# ----------------------------
with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print("Sorting complete — saved as QBDataCube_sorted.csv")
