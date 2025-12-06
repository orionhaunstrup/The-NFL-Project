import requests
import re
import csv
from time import sleep

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def clean_value(s):
    s = s.strip()
    if s in ("", "--"):
        return s
    if "/" in s:
        return s
    s = s.replace(',', '')
    s = re.sub(r'[^\d\.]', '', s)
    if s == "":
        return ""
    if '.' in s:
        return float(s)
    return int(s)

def scrape_kicking_year(year):
    url = f"https://www.footballdb.com/statistics/nfl/player-stats/kicking/{year}"
    print(f"Fetching {year}: {url}")
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    lines = resp.text.splitlines()
    data_rows = []

    for line in lines:
        if line.strip().startswith('<tr class="row'):
            name_match = re.search(r'title="([^"]+) Stats"', line)
            if not name_match:
                continue
            player_name = name_match.group(1)
            raw_values = re.findall(r'<td[^>]*>([^<]*)</td>', line)
            filtered_values = [v for v in raw_values if v not in (None, "")]
            cleaned_values = [clean_value(v) for v in filtered_values]
            if year <= 1969:
                if len(cleaned_values) == 11:
                    cleaned_values.pop(0)
            data_rows.append([player_name] + cleaned_values)

    print(f"  Found {len(data_rows)} players for {year}")
    return data_rows

def scrape_kicking_all_years(start=2024, end=1940):
    for year in range(start, end - 1, -1):
        headers = ["Player Name", "Games Played", "Extra Points Kicks", "Field Goals",
                   "0-19", "20-29", "30-39", "40-49", "50+", "Long", "Points"] if year >= 1970 else \
                  ["Player Name", "Extra Points Kicks", "Field Goals",
                   "0-19", "20-29", "30-39", "40-49", "50+", "Long", "Points"]

        year_rows = scrape_kicking_year(year)
        out_filename = f"FootballDB_Kicking_{year}.csv"
        with open(out_filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(year_rows)

        print(f"Saved {len(year_rows)} rows to {out_filename}")
        sleep(0.5)

if __name__ == "__main__":
    scrape_kicking_all_years()
