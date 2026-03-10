import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

BASE_URL = "https://cbsfm.ug/wp-json/wp/v2/posts"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_Luganda_posts(category_id, target_count=1000):
    articles = []
    page = 1

    while len(articles) < target_count:
        print(f"Fetching page {page}...")

        params = {
            "categories": category_id,
            "per_page": 100,   # WordPress max
            "page": page
        }

        response = requests.get(BASE_URL, headers=HEADERS, params=params)

        if response.status_code != 200:
            print("No more pages available.")
            break

        data = response.json()
        if not data:
            break

        for post in data:
            title = BeautifulSoup(post["title"]["rendered"], "html.parser").get_text()
            content = BeautifulSoup(post["content"]["rendered"], "html.parser").get_text()

            if len(content) > 150:
                articles.append({
                    "title": title,
                    "content": content,
                    "url": post["link"]
                })

            if len(articles) >= target_count:
                break

        page += 1
        time.sleep(1)

    return articles[:target_count]


def main():
    AMAWULIRE_ID = 2

    print("Scraping 1000 Luganda articles from CBS...\n")

    Luganda_articles = get_Luganda_posts(AMAWULIRE_ID, target_count=1000)

    df = pd.DataFrame(Luganda_articles)
    df.to_csv("cbs_Luganda_1000.csv", index=False, encoding="utf-8")

    print(f"\nSaved {len(df)} Luganda articles.")


if __name__ == "__main__":
    main()
