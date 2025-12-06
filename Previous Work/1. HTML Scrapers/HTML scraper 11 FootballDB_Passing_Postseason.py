import requests
import re
import csv
from time import sleep

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def clean_number(s):
    s = s.strip()
    if s == "--" or s == "":
        return s
    s = s.replace(',', '')
    s = re.sub(r'[^\d\.]', '', s)
    if s == "":
        return ""
    if '.' in s:
        return float(s)
    return int(s)

def scrape_year(year):
    url = f"https://www.footballdb.com/statistics/nfl/player-stats/passing/{year}/postseason?sort=passrate"
    print(f"Fetching {year}: {url}")

    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    lines = resp.text.splitlines()

    rows = []

    for line in lines:
        if line.strip().startswith('<tr class="row'):
            name_match = re.search(r'title="([^"]+) Stats"', line)
            if not name_match:
                continue
            player_name = name_match.group(1)

            raw = re.findall(r'<td[^>]*>([\d,\.]+[t]?|--)?</td>', line)
            filtered = [v for v in raw if v not in (None, "")]
            cleaned = [clean_number(v) for v in filtered]

            if year in (1967, 1966):
                if len(cleaned) == 13:
                    cleaned.insert(0, "N/A")

            rows.append([player_name] + cleaned)

    print(f"  Found {len(rows)} players for {year}")
    return rows

def scrape_all_years(start=2024, end=1966):
    headers_modern = [
        "player name", "games played", "attempts", "completions", "completion %",
        "passing yards", "yards per attempt", "touchdowns", "touchdown %",
        "interceptions", "interception %", "Long", "Sacks",
        "Sack loss yards", "QB rating"
    ]

    headers_old = [
        "player name", "attempts", "completions", "completion %",
        "passing yards", "yards per attempt", "touchdowns", "touchdown %",
        "interceptions", "interception %", "Long", "Sacks",
        "Sack loss yards", "QB rating"
    ]

    for year in range(start, end - 1, -1):
        rows = scrape_year(year)
        headers = headers_modern if year >= 1968 else headers_old
        filename = f"nfl_playoffs_passing_{year}.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        print(f"Saved {len(rows)} rows → {filename}")
        sleep(0.5)

if __name__ == "__main__":
    scrape_all_years()
