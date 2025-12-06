import csv
from pathlib import Path

PASSING_FILE = Path("NFL_Passing_2024.csv")
RUSHING_FILE = Path("NFL_Rushing_2024.csv")
OUTFILE = Path("QBDataCube.csv")

def extract_headers(csv_path):
    """Read and return the header row of a CSV file."""
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
    return header

def build_header():
    # Load column names from the source files
    passing_cols = extract_headers(PASSING_FILE)
    rushing_cols = extract_headers(RUSHING_FILE)

    # Build the new Data Cube header
    return ["PLAYER NAME", "YEAR"] + passing_cols + rushing_cols

def write_qb_datacube(header):
    with OUTFILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

    print(f"Created QBDataCube.csv with {len(header)} columns.")

if __name__ == "__main__":
    header = build_header()
    write_qb_datacube(header)
