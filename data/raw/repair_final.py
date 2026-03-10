import re
import csv

input_path = "uganda_fake_news_v2.csv"
output_path = "uganda_fake_news_v2_clean_final.csv"

pattern_date = re.compile(r"\d{4}-\d{2}-\d{2}")

with open(input_path, "r", encoding="utf-8") as infile, \
     open(output_path, "w", encoding="utf-8", newline="") as outfile:

    writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)

    # Write clean header
    writer.writerow(["id", "text", "label", "source", "language", "date_collected"])

    lines = infile.readlines()

    for line in lines[1:]:  # Skip header
        line = line.strip()

        if not line:
            continue

        parts = [p.strip().strip('"') for p in line.split(",")]

        # ID is always first
        id_col = parts[0]

        # Date is always the last valid YYYY-MM-DD in row
        date_collected = None
        for p in reversed(parts):
            if pattern_date.match(p):
                date_collected = p
                break

        if not date_collected:
            continue  # skip broken row

        # Language is right before date
        date_index = parts.index(date_collected)
        language = parts[date_index - 1]

        # Source is before language
        source = parts[date_index - 2]

        # Label is before source
        label = parts[date_index - 3]

        # Everything between id and label is text
        text = ",".join(parts[1:date_index - 3]).strip()

        writer.writerow([
            id_col,
            text,
            label,
            source,
            language,
            date_collected
        ])

print("Dataset fully rebuilt successfully.")