import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "https://www.bukedde.co.ug"
CATEGORY_URL = "https://www.bukedde.co.ug/category/amawulire?id=2"
TARGET_ARTICLES = 250



def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.set_page_load_timeout(60)

    return driver


def get_article_links(driver):
    links = set()
    page = 1

    while len(links) < TARGET_ARTICLES:
        url = f"{CATEGORY_URL}&page={page}"
        print(f"Scanning page {page}...")

        try:
            driver.get(url)

            # Wait until links are present
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "a"))
            )

            soup = BeautifulSoup(driver.page_source, "html.parser")

            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.startswith("/amawulire/"):
                    links.add(BASE_URL + href)

            print(f"Collected so far: {len(links)} links")

            page += 1
            time.sleep(1)

            if page > 40:  
                break

        except TimeoutException:
            print("Page load timeout. Retrying...")
            continue

    return list(links)[:TARGET_ARTICLES]



def scrape_article(driver, url):
    try:
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")

        title_tag = soup.find("h1", class_="main_heading")
        title = title_tag.get_text(strip=True) if title_tag else ""

        content_div = soup.find("div", class_="align-center")
        article_text = ""

        if content_div:
            paragraphs = content_div.find_all("p")
            article_text = " ".join(
                p.get_text(strip=True) for p in paragraphs
            )

        return title, article_text

    except Exception as e:
        print("Error scraping:", url)
        return "", ""


def main():
    driver = setup_driver()

    print("Starting Bukedde scraper...\n")
    links = get_article_links(driver)

    print(f"\nCollected {len(links)} article links.\n")

    with open("bukedde_Luganda.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["title", "text", "language", "source"])

        for i, link in enumerate(links):
            print(f"Scraping {i+1}/{len(links)}")
            title, text = scrape_article(driver, link)

            if title and text:
                writer.writerow([title, text, "Luganda", "bukedde"])

            time.sleep(1)

    driver.quit()
    print("\nFinished scraping Bukedde.")


if __name__ == "__main__":
    main()
