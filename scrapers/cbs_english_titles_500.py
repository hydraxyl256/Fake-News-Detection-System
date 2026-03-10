import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

BASE_URL = "https://cbsfm.ug/wp-json/wp/v2/posts"
HEADERS = {"User-Agent": "Mozilla/5.0"}

ENGLISH_CATEGORIES = [6, 10, 8]  # Business, Politics, BUGANDA

def get_english_titles(target_count=500):
    articles = []
    
    for category_id in ENGLISH_CATEGORIES:
        page = 1

        while len(articles) < target_count:
            print(f"Fetching category {category_id} page {page}...")

            params = {
                "categories": category_id,
                "per_page": 100,
                "page": page
            }

            response = requests.get(BASE_URL, headers=HEADERS, params=params)

            if response.status_code != 200:
                break

            data = response.json()
            if not data:
                break

            for post in data:
                title = BeautifulSoup(post["title"]["rendered"], "html.parser").get_text()

                articles.append({
                    "title": title,
                    "language": "english"
                })

                if len(articles) >= target_count:
                    break

            page += 1
            time.sleep(1)

        if len(articles) >= target_count:
            break

    return articles[:target_count]


def main():
    print("Scraping 500 English titles...\n")

    articles = get_english_titles()
    df = pd.DataFrame(articles)

    df.to_csv("cbs_english_titles_500.csv", index=False, encoding="utf-8")

    print(f"\nSaved {len(df)} English titles.")


if __name__ == "__main__":
    main()
