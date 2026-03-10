# africacheck_dubawa_false_scraper_simple.py
import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ====================
# Config
# ====================
START_ID = 200
TOTAL_ARTICLES = 750  # total combined
OUTPUT_FILE = "africa_false_news_simple.csv"
LANGUAGE = "English"
LABEL = "FALSE"
PLATFORM = "website"
DATE_COLLECTED = datetime.today().strftime("%Y-%m-%d")

# Africa Check & Dubawa URLs
AFRICA_CHECK_URL = "https://africacheck.org/fact-checks/"
DUBAWA_URL = "https://dubawa.org/category/fact-check/"

# Selenium Chrome setup
chrome_options = Options()
chrome_options.add_argument("--headless")  # run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

# ====================
# Scraper functions
# ====================
def scrape_africacheck(max_count):
    print("Scraping Africa Check False news...")
    titles = []
    driver.get(AFRICA_CHECK_URL)
    time.sleep(3)

    while len(titles) < max_count:
        # wait for articles
        try:
            articles = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article h2 a"))
            )
        except:
            break

        for a in articles:
            title = a.text.strip()
            if title and title not in titles:
                titles.append(title)
                if len(titles) >= max_count:
                    break

        # go to next page
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
            next_button.click()
            time.sleep(2)
        except:
            break

    print(f"Africa Check collected: {len(titles)} articles")
    return titles

def scrape_dubawa(max_count):
    print("Scraping Dubawa False news...")
    titles = []
    driver.get(DUBAWA_URL)
    time.sleep(3)

    while len(titles) < max_count:
        try:
            articles = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2.entry-title a"))
            )
        except:
            break

        for a in articles:
            title = a.text.strip()
            if title and title not in titles:
                titles.append(title)
                if len(titles) >= max_count:
                    break

        # go to next page
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, ".nav-previous a")
            next_button.click()
            time.sleep(2)
        except:
            break

    print(f"Dubawa collected: {len(titles)} articles")
    return titles

# ====================
# Main logic
# ====================
all_titles = []

# Split the total articles evenly
half_count = TOTAL_ARTICLES // 2
all_titles.extend(scrape_africacheck(half_count))
all_titles.extend(scrape_dubawa(TOTAL_ARTICLES - len(all_titles)))

# Write to CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "id", "text", "label", "source", "platform_type", "language", "date_collected"
    ])
    writer.writeheader()
    for idx, title in enumerate(all_titles, START_ID):
        writer.writerow({
            "id": f"UG_FALSE_{idx:03d}",
            "text": title,
            "label": LABEL,
            "source": "Africa Check/Dubawa",
            "platform_type": PLATFORM,
            "language": LANGUAGE,
            "date_collected": DATE_COLLECTED
        })

print(f"Saved {len(all_titles)} articles to {OUTPUT_FILE}")
driver.quit()
