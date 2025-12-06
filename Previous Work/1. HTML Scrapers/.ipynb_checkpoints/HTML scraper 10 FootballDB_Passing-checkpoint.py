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
    url = f"https://www.footballdb.com/statistics/nfl/player-stats/passing/{year}"
    print(f"Fetching {year}: {url}")
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    html = resp.text
    lines = html.splitlines()

    data_rows = []

    for line in lines:
        if line.strip().startswith('<tr class="row'):
            name_match = re.search(r'title="([^"]+) Stats"', line)
            if not name_match:
                continue
            player_name = name_match.group(1)

            raw_values = re.findall(r'<td[^>]*>([\d,\.]+[t]?|--)?</td>', line)
            filtered_values = [v for v in raw_values if v not in (None, "")]
            cleaned_numbers = [clean_number(v) for v in filtered_values]

            if year < 1966:
                if len(cleaned_numbers) == 13:
                    cleaned_numbers.insert(12, "N/A")
                    cleaned_numbers.insert(13, "N/A")
            if year == 1940:
                if len(cleaned_numbers) == 13:
                    cleaned_numbers.insert(11, "N/A")

            data_rows.append([player_name] + cleaned_numbers)

    print(f"  Found {len(data_rows)} players for {year}")
    return data_rows

def scrape_all_years(start=2024, end=1940):
    headers_modern = ["player name", "games played", "attempts", "completions", "completion %",
                      "passing yards", "yards per attempt", "touchdowns", "touchdown %",
                      "interceptions", "interception %", "Long", "Sacks",
                      "Sack loss yards", "QB rating"]

    headers_old = ["player name", "attempts", "completions", "completion %",
                   "passing yards", "yards per attempt", "touchdowns", "touchdown %",
                   "interceptions", "interception %", "Long", "Sacks",
                   "Sack loss yards", "QB rating"]

    for year in range(start, end - 1, -1):
        year_rows = scrape_year(year)
        out_filename = f"nfl_passing_{year}.csv"
        headers = headers_modern if year >= 1970 else headers_old
        with open(out_filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(year_rows)
        print(f"Saved {len(year_rows)} rows to {out_filename}")
        sleep(0.5)

if __name__ == "__main__":
    scrape_all_years()
