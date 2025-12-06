import csv
from pathlib import Path

OUTPUT = Path("QBDataCube.csv")

def load_players_and_rows(csv_path):
    """
    Returns:
        header: list of column names
        names: list of PLAYER NAME strings
        rows: dict mapping PLAYER NAME -> full row (including PLAYER NAME col)
    If csv missing, returns empty header, names, and rows.
    """
    if not csv_path.exists():
        return [], [], {}

    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        names = []
        rows = {}

        for row in reader:
            if not row:
                continue
            name = row[0].strip()
            if name == "":
                continue
            names.append(name)
            rows[name] = row

        return header, names, rows


with OUTPUT.open("a", newline="", encoding="utf-8") as out:
    writer = csv.writer(out)

    for year in range(1940, 2025):

        passing_file = Path(f"NFL_Passing_{year}.csv")
        rushing_file = Path(f"NFL_Rushing_{year}.csv")

        # Load passing
        pass_header, pass_names, pass_rows = load_players_and_rows(passing_file)
        # Load rushing
        rush_header, rush_names, rush_rows = load_players_and_rows(rushing_file)

        # Unique set of every player found in either file
        all_players = sorted(set(pass_names) | set(rush_names))

        # Pre-compute blank placeholders for missing data
        blank_passing = ["*"] * len(pass_header)
        blank_rushing = ["*"] * len(rush_header)

        print(f"YEAR {year}: {len(all_players)} players")

        for name in all_players:

            row_out = []

            # -----------------------------
            # First two columns: name, year
            # -----------------------------
            row_out.append(name)
            row_out.append(year)

            # -----------------------------
            # PASSING SECTION (ALL columns)
            # -----------------------------
            if name in pass_rows:
                row_out.extend(pass_rows[name])
            else:
                row_out.extend(blank_passing)

            # -----------------------------
            # RUSHING SECTION (ALL columns)
            # -----------------------------
            if name in rush_rows:
                row_out.extend(rush_rows[name])
            else:
                row_out.extend(blank_rushing)

            writer.writerow(row_out)
