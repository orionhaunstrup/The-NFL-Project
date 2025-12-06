from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import re

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

player_pattern = re.compile(r"players/([a-zA-Z0-9\-]+)")
number_pattern = re.compile(r"^-?\d+(\.\d+)?$")

header = [
    "Name", "Receptions", "Receiving Yards", "Touchdowns", "20+", "40+",
    "Long", "Receiving 1st Downs", "Receiving Fumbles",
    "Yards After Catch Per Reception", "Targets"
]

for year in range(2006, 1969, -1):
    print(f"\nScraping NFL Receiving stats for {year}...")

    url = f"https://www.nfl.com/stats/player-stats/category/receiving/{year}/reg/all/receivingreceptions/DESC"
    driver.get(url)

    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(., 'ACCEPT','accept'), 'accept')]"))
        )
        cookie_button.click()
        time.sleep(1)
    except:
        pass

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )
    except:
        print("Table didn't load — skipping year.")
        continue

    rows = []
    prev_first_player = None

    while True:
        html = driver.page_source
        text = html.splitlines()

        current_player = None
        current_numbers = []
        page_rows = []

        for line in text:
            line = line.strip()
            pmatch = player_pattern.search(line)
            if pmatch:
                if current_player:
                    page_rows.append([current_player] + current_numbers)
                current_player = pmatch.group(1)
                current_numbers = []
            elif number_pattern.match(line):
                current_numbers.append(line)

        if current_player:
            page_rows.append([current_player] + current_numbers)

        if page_rows:
            first_receiver = page_rows[0][0]
            formatted_name = " ".join([w.capitalize() for w in first_receiver.split('-')])
            print("First player this page:", formatted_name)

        first_player = page_rows[0][0] if page_rows else None

        if first_player == prev_first_player:
            print("Same first player — waiting 20s to confirm next page...")
            time.sleep(20)
            html = driver.page_source
            text = html.splitlines()
            page_rows = []
            current_player = None
            current_numbers = []
            for line in text:
                line = line.strip()
                pmatch = player_pattern.search(line)
                if pmatch:
                    if current_player:
                        page_rows.append([current_player] + current_numbers)
                    current_player = pmatch.group(1)
                    current_numbers = []
                elif number_pattern.match(line):
                    current_numbers.append(line)
            if current_player:
                page_rows.append([current_player] + current_numbers)
            first_player = page_rows[0][0] if page_rows else None
            if first_player == prev_first_player:
                print("Last page reached (confirmed after wait).")
                break

        prev_first_player = first_player

        for i, row in enumerate(page_rows):
            row[0] = " ".join([word.capitalize() for word in row[0].split('-')])
        rows.extend(page_rows)

        try:
            driver.execute_script("""
                const nextBtn = [...document.querySelectorAll('button, a')]
                                .find(el => el.innerText.trim() === 'Next Page');
                if (nextBtn && !nextBtn.disabled) {
                    nextBtn.scrollIntoView();
                    nextBtn.click();
                } else {
                    throw 'No more pages';
                }
            """)
            print("Clicked NEXT PAGE, waiting 10s...")
            time.sleep(10)
        except:
            print("Last page reached (no button found).")
            break

    filename = f"NFL_Receiving_{year}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"Saved {filename} with {len(rows)} players")

driver.quit()
print("\nFinished scraping all NFL Receiving stats from 2006 to 1970.")
