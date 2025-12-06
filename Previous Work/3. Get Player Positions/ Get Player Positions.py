import csv
import requests
import re
import os
import json
from time import sleep

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

ACCEPTABLE_POSITIONS = {"QB", "RB", "FB", "HB", "Unknown"}

CACHE_FILE = "player_position_cache.json"

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        position_cache = json.load(f)
else:
    position_cache = {}

def save_cache():
    """Write the cache to disk after each lookup."""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(position_cache, f, indent=2)

def name_to_url(name):
    return name.strip().lower().replace(" ", "-")

def get_player_position(player_url, player_name):
    """Fetch NFL.com player page and extract position, using persistent cache."""
    if player_name in position_cache:
        return position_cache[player_name]

    try:
        resp = requests.get(player_url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        html = resp.text

        match = re.search(
            r'<span class="nfl-c-player-header__position">\s*([A-Z]+)\s*</span>',
            html
        )
        if match:
            position = match.group(1)
        else:
            position = "Unknown"

    except Exception:
        position = "Unknown"

    position_cache[player_name] = position
    save_cache()

    return position

def collect_player_positions(csv_folder, output_txt):
    all_players = set()

    # Find all the CSV files
    for filename in os.listdir(csv_folder):
        if filename.lower().endswith(".csv"):
            path = os.path.join(csv_folder, filename)
            print(f"Reading {filename}...")

            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)

                for row in reader:
                    if row and row[0].strip():
                        all_players.add(row[0].strip())

    all_players = sorted(all_players)
    total = len(all_players)

    print(f"\nFound {total} unique players.\n")

    # Resume output file if it exists
    seen_players = set()
    if os.path.exists(output_txt):
        print("Resuming from previous output...")
        with open(output_txt, "r", encoding="utf-8") as f:
            for line in f:
                if " - " in line:
                    name = line.split(" - ")[0].strip()
                    seen_players.add(name)

    # Open output file for appending
    out = open(output_txt, "a", encoding="utf-8")

    milestone = 1

    # Process each player
    for idx, name in enumerate(all_players, start=1):

        if name in seen_players:
            # Already written to txt file
            continue

        url_name = name_to_url(name)
        player_url = f"https://www.nfl.com/players/{url_name}/"
        position = get_player_position(player_url, name)

        # Write line immediately -> crash-safe
        out.write(f"{name} - {position}\n")
        out.flush()

        # Percent progress
        progress = (idx / total) * 100
        if progress >= milestone:
            print(f"{milestone}% complete...")
            milestone += 1

        sleep(0.2)

    out.close()
    print("\nDone! All player positions saved.\n")



if __name__ == "__main__":
    collect_player_positions(".", "player_positions.txt")

