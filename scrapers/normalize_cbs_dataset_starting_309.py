import pandas as pd
from datetime import datetime

def normalize_csv(
    input_file,
    output_file,
    text_column,
    language,
    start_id=309,
    source_name="CBS FM",
    platform_type="traditional_media"
):
    # Load raw file
    df = pd.read_csv(input_file)

    # Keep only the text column
    df = df[[text_column]].copy()

    # Rename to required schema
    df.rename(columns={text_column: "text"}, inplace=True)

    # Generate IDs like UG_TRUE_309, UG_TRUE_310 ...
    df["id"] = [f"UG_TRUE_{str(i + start_id).zfill(3)}" for i in range(len(df))]

    # Add fixed columns
    df["label"] = "TRUE"
    df["source"] = source_name
    df["platform_type"] = platform_type
    df["language"] = language
    df["date_collected"] = datetime.today().strftime("%Y-%m-%d")

    # Reorder columns
    df = df[
        ["id", "text", "label", "source", "platform_type", "language", "date_collected"]
    ]

    # Save
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"✅ Saved normalized dataset to {output_file} ({len(df)} rows)")

# Example usage
if __name__ == "__main__":
    # Luganda news starting from 309
    normalize_csv(
        input_file="cbs_luganda_titles_1000.csv",
        output_file="cbs_luganda_clean.csv",
        text_column="title",
        language="luganda",
        start_id=309
    )

    # English news starting from 1309 
    normalize_csv(
        input_file="cbs_english_titles_500.csv",
        output_file="cbs_english_clean.csv",
        text_column="title",
        language="english",
        start_id=1309
    )
