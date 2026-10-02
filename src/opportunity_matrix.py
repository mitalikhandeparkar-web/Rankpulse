import pandas as pd


def classify_opportunity(row):

    score = row["opportunity_score"]
    position = row["your_position"]

    # High opportunity
    if score >= 75 and position > 10:
        return "High Opportunity"

    # Medium opportunity
    elif score >= 55:
        return "Medium Opportunity"

    # Low opportunity
    else:
        return "Low Opportunity"


def create_opportunity_matrix(file_path):

    df = pd.read_csv(file_path)

    # Classify every keyword
    df["opportunity_level"] = df.apply(
        classify_opportunity,
        axis=1
    )

    # Sort highest opportunity first
    df = df.sort_values(
        by="opportunity_score",
        ascending=False
    )

    return df