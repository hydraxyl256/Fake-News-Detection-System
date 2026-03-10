import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

BASE_URL = "https://cbsfm.ug/wp-json/wp/v2/posts"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_luganda_titles(category_id=2, target_count=1000):
    articles = []
    page = 1

    while len(articles) < target_count:
        print(f"Fetching Luganda page {page}...")

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
                "language": "luganda"
            })

            if len(articles) >= target_count:
                break

        page += 1
        time.sleep(1)

    return articles[:target_count]


def main():
    print("Scraping 1000 Luganda titles...\n")

    articles = get_luganda_titles()
    df = pd.DataFrame(articles)

    df.to_csv("cbs_luganda_titles_1000.csv", index=False, encoding="utf-8")

    print(f"\nSaved {len(df)} Luganda titles.")


if __name__ == "__main__":
    main()
