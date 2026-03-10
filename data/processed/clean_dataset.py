import pandas as pd

INPUT_FILE = "uganda_fake_news_v2_cleaned.csv"
OUTPUT_FILE = "uganda_fake_news_v3_final.csv"

# Load dataset
df = pd.read_csv(INPUT_FILE)


# Drop completely empty columns

df = df.dropna(axis=1, how="all")


# Remove unwanted columns safely

columns_to_keep = [
    "id",
    "text",
    "label",
    "source",
    "platform_type",
    "language",
    "date_collected"
]

df = df[[col for col in columns_to_keep if col in df.columns]]


# Ensure correct column order

df = df[columns_to_keep]


# Remove empty rows

df = df[df["text"].notna()]
df = df[df["text"].str.strip() != ""]


#Save WITHOUT trailing column

df.to_csv(OUTPUT_FILE, index=False)

print("Final cleaned dataset saved.")
print("Columns:", df.columns.tolist())
print("Total rows:", len(df))
