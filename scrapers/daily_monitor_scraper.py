import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://www.monitor.co.ug"
CATEGORY_URL = "https://www.monitor.co.ug/uganda/news"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

TARGET_ARTICLES = 250


def get_article_links():
    links = set()
    page = 1

    while len(links) < TARGET_ARTICLES:
        url = f"{CATEGORY_URL}?page={page}"
        print(f"Scanning page {page}...")

        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.find_all("a", href=True):
            href = a["href"]

            if "/uganda/news/" in href and href.startswith("/"):
                full_link = BASE_URL + href
                links.add(full_link)

        page += 1
        time.sleep(1)

        if page > 40:
            break

    return list(links)[:TARGET_ARTICLES]


def scrape_article(url):
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        # Title
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # Article body (Monitor usually uses article tag)
        article_tag = soup.find("article")
        article_text = ""

        if article_tag:
            paragraphs = article_tag.find_all("p")
            article_text = " ".join(
                p.get_text(strip=True) for p in paragraphs
            )

        return title, article_text

    except Exception as e:
        print("Error scraping:", url)
        return "", ""


def main():
    links = get_article_links()
    print(f"Collected {len(links)} article links.")

    with open("daily_monitor_english.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["title", "text", "language", "source"])

        for i, link in enumerate(links):
            print(f"Scraping {i+1}/{len(links)}")
            title, text = scrape_article(link)

            if title and text:
                writer.writerow([title, text, "english", "daily_monitor"])

            time.sleep(1)

    print("Finished scraping Daily Monitor.")


if __name__ == "__main__":
    main()
