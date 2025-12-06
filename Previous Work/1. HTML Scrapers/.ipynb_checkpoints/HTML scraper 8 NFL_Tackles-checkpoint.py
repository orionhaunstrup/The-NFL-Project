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
stat_pattern = re.compile(r"^-?\d+(?:\.\d+)?$")

header = ["Name", "Combined", "Assists", "Solos", "Sacks"]
EXPECTED_NUMERIC_COUNT = len(header) - 1

for year in range(1983, 1969, -1):
    print(f"Scraping NFL Tackles stats for {year}...")

    url = f"https://www.nfl.com/stats/player-stats/category/tackles/{year}/reg/all/defensivecombinetackles/desc"
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
            elif stat_pattern.match(line):
                current_numbers.append(line)

        if current_player:
            page_rows.append([current_player] + current_numbers)

        if page_rows:
            first_player = page_rows[0][0]
        else:
            first_player = None

        if first_player == prev_first_player:
            print("Last page reached.")
            break

        prev_first_player = first_player

        for i, row in enumerate(page_rows):
            name = " ".join([word.capitalize() for word in row[0].split('-')])
            nums = row[1:]
            nums = [n.replace("−", "-").replace(",", "") for n in nums]

            if len(nums) < EXPECTED_NUMERIC_COUNT:
                nums += ["N/A"] * (EXPECTED_NUMERIC_COUNT - len(nums))
            elif len(nums) > EXPECTED_NUMERIC_COUNT:
                nums = nums[:EXPECTED_NUMERIC_COUNT]

            page_rows[i] = [name] + nums

        rows.extend(page_rows)

        try:
            driver.execute_script("""
                const nextBtn = [...document.querySelectorAll('button, a')]
                    .find(el => el.innerText.trim().toLowerCase() === 'next page');
                if (nextBtn && !nextBtn.disabled) {
                    nextBtn.scrollIntoView();
                    nextBtn.click();
                } else {
                    throw 'No more pages';
                }
            """)
            print("Clicked NEXT PAGE, waiting...")
            time.sleep(10)
        except:
            print("Last page reached.")
            break

    filename = f"NFL_Tackles_{year}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"Saved {filename} with {len(rows)} players")

driver.quit()
print("Finished scraping NFL Tackles stats.")
