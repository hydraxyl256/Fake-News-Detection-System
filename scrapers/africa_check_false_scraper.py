from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
from datetime import datetime
import time

# ================= CONFIG =================
TOTAL_ARTICLES = 750
START_ID = 950
OUTPUT_FILE = "africa_check_false_news.csv"
DATE_COLLECTED = datetime.today().strftime("%Y-%m-%d")





BASE_URL = "https://africacheck.org/fact-checks/"


def scrape_africa_check():
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
    driver.get(BASE_URL)
    collected = []
    page = 1

    while len(collected) < TOTAL_ARTICLES:
        print(f"Scanning page {page}...")
        articles = driver.find_elements(By.CSS_SELECTOR, "article h2 a")
        for a in articles:
            title = a.text.strip()
            if title:
                collected.append(title)
            if len(collected) >= TOTAL_ARTICLES:
                break

        # Try to click next page
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "a.next.page-numbers")
            next_btn.click()
            time.sleep(2)
            page += 1
        except:
            print("No more pages or failed to navigate.")
            break

    driver.quit()
    return collected

def save_to_csv(titles):
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "text", "label", "source",
            "platform_type", "language", "date_collected"
        ])
        writer.writeheader()
        current_id = START_ID
        for title in titles:
            writer.writerow({
                "id": f"UG_FALSE_{current_id}",
                "text": title,
                "label": "FALSE",
                "source": "Africa Check",
                "platform_type": "Website",
                "language": "English",
                "date_collected": DATE_COLLECTED
            })
            current_id += 1
    print(f"\nSaved {len(titles)} articles to {OUTPUT_FILE}")

if __name__ == "__main__":
    titles = scrape_africa_check()
    save_to_csv(titles)
