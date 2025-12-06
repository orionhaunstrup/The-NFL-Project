from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = "https://www.nfl.com/stats/player-stats/category/passing/2024/reg/all/passingyards/desc"
driver.get(url)

try:
    cookie_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(., 'ACCEPT','accept'), 'accept')]"))
    )
    print("Cookie popup found — clicking Accept...")
    cookie_button.click()
    time.sleep(1)
except:
    print("No cookie popup found.")

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
)
print("First table loaded")

def get_player_names():
    rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr"))
    )
    names = []
    for row in rows:
        try:
            name_cell = row.find_element(By.CSS_SELECTOR, "a.d3-o-player-fullname")
            names.append(name_cell.text.strip())
        except:
            continue
    return names

page1_names = get_player_names()
print("\nPage 1 Players:")
for name in page1_names:
    print(" -", name)

try:
    driver.execute_script("""
        const nextBtn = [...document.querySelectorAll('button, a')]
                        .find(el => el.innerText.trim() === 'Next Page');
        if (nextBtn) {
            nextBtn.scrollIntoView();
            nextBtn.click();
        } else {
            throw 'Next Page button not found';
        }
    """)
    print("\nClicked NEXT PAGE... waiting for page 2...")
except Exception as e:
    print("Couldn't find or click NEXT PAGE button:", e)
    driver.quit()
    raise SystemExit

WebDriverWait(driver, 15).until_not(
    EC.text_to_be_present_in_element((By.CSS_SELECTOR, "tbody"), page1_names[0])
)

page2_names = get_player_names()
print("\nPage 2 Players:")
for name in page2_names:
    print(" -", name)

print("\nSuccess! Both pages scraped.")
time.sleep(5)
driver.quit()
