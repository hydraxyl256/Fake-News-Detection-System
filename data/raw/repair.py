import csv

input_path = "uganda_fake_news_v2.csv"
output_path = "uganda_fake_news_v2_fixed.csv"

with open(input_path, "r", encoding="utf-8") as infile, \
     open(output_path, "w", encoding="utf-8", newline="") as outfile:

    reader = infile.readlines()
    writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)

    # Write correct header
    writer.writerow(["id", "text", "label", "source", "language", "date_collected"])

    for line in reader[1:]: 
        parts = [p.strip() for p in line.strip().split(",")]

        # Skip bad or empty lines
        if len(parts) < 6:
            continue

        # First column
        id_col = parts[0]

        # Last 4 structured columns
        label = parts[-4]
        source = parts[-3]
        language = parts[-2]
        date_collected = parts[-1]

        # Everything between id and label is text
        text = ",".join(parts[1:-4])

        writer.writerow([
            id_col,
            text,
            label,
            source,
            language,
            date_collected
        ])

print("File repaired successfully.")