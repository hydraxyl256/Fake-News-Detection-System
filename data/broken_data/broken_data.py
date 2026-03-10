with open("../data/raw/uganda_fake_news_v2.csv", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if 105 <= i <= 115:
            print(i, line)