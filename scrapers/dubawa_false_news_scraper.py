import requests
import csv
from datetime import datetime

# Configuration
BASE_URL = "https://dubawa.org/wp-json/wp/v2/posts"
PER_PAGE = 100  # Max per page
TOTAL_ARTICLES = 750
CSV_FILE = "africa_false_news.csv"
START_ID = 200

# Metadata defaults
SOURCE = "Dubawa"
PLATFORM_TYPE = "Website"
LABEL = "FALSE"
LANGUAGE = "English"
DATE_COLLECTED = datetime.today().strftime("%Y-%m-%d")

def fetch_posts(page):
    """Fetch posts from Dubawa JSON API for a given page."""
    params = {"per_page": PER_PAGE, "page": page}
    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch page {page}: {e}")
        return []

def main():
    collected = []
    current_id = START_ID
    page = 1

    while len(collected) < TOTAL_ARTICLES:
        posts = fetch_posts(page)
        if not posts:
            print(f"No more posts found at page {page}. Stopping.")
            break

        for post in posts:
            title = post.get("title", {}).get("rendered", "").strip()
            if not title:
                continue

            article = {
                "id": f"UG_FALSE_{current_id}",
                "text": title,
                "label": LABEL,
                "source": SOURCE,
                "platform_type": PLATFORM_TYPE,
                "language": LANGUAGE,
                "date_collected": DATE_COLLECTED,
            }
            collected.append(article)
            current_id += 1

            if len(collected) >= TOTAL_ARTICLES:
                break

        print(f"Collected {len(collected)} articles so far...")
        page += 1

    # Save to CSV
    if collected:
        keys = ["id", "text", "label", "source", "platform_type", "language", "date_collected"]
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(collected)

        print(f"Saved {len(collected)} articles to {CSV_FILE}")
    else:
        print("No articles collected.")

if __name__ == "__main__":
    main()
