from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import re

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.nfl.com/stats/player-stats/category/passing/2024/reg/all/passingyards/DESC"
driver.get(url)
time.sleep(3)

player_pattern = re.compile(r"players/([a-zA-Z0-9\-]+)")
number_pattern = re.compile(r"^\s*\d+(\.\d+)?\s*$")

rows = []

while True:
    html = driver.page_source
    text = html.splitlines()
    
    current_player = None
    current_numbers = []
    
    for line in text:
        line = line.strip()
        pmatch = player_pattern.search(line)
        if pmatch:
            if current_player:
                rows.append([current_player] + current_numbers)
            current_player = pmatch.group(1)
            current_numbers = []
        elif number_pattern.match(line):
            current_numbers.append(line)
    
    if current_player:
        rows.append([current_player] + current_numbers)
    
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "a.d3-o-pagination__next")
        if "disabled" in next_button.get_attribute("class"):
            break
        next_button.click()
        time.sleep(2)
    except:
        break

with open("Passing_2024.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

driver.quit()
print("Saved Passing_2024.csv with", len(rows), "players")
