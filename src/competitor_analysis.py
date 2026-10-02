import pandas as pd


def analyze_competitors(file_path):

    df = pd.read_csv(file_path)

    # Calculate SEO score gap
    your_score = df.iloc[0]["seo_score"]

    df["score_gap"] = (
        df["seo_score"] - your_score
    )

    # Calculate keyword gap
    your_keywords = df.iloc[0]["organic_keywords"]

    df["keyword_gap"] = (
        df["organic_keywords"] - your_keywords
    )

    # Sort competitors by SEO score
    df = df.sort_values(
        by="seo_score",
        ascending=False
    )

    return df