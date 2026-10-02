import pandas as pd


def calculate_seo_score(row):

    score = 0

    # --------------------------------
    # 1. HTTPS - 15 points
    # --------------------------------

    if row["https_enabled"]:
        score += 15


    # --------------------------------
    # 2. Page Title - 15 points
    # --------------------------------

    title = str(row["title"]).strip()

    if title:

        title_length = len(title)

        if 30 <= title_length <= 60:
            score += 15

        elif 20 <= title_length <= 70:
            score += 10

        else:
            score += 5


    # --------------------------------
    # 3. Meta Description - 15 points
    # --------------------------------

    meta = str(
        row["meta_description"]
    ).strip()

    if meta:

        meta_length = len(meta)

        if 120 <= meta_length <= 160:
            score += 15

        elif 80 <= meta_length <= 180:
            score += 10

        else:
            score += 5


    # --------------------------------
    # 4. H1 Structure - 15 points
    # --------------------------------

    if row["h1_count"] == 1:

        score += 15

    elif row["h1_count"] > 1:

        score += 8


    # --------------------------------
    # 5. Image ALT Coverage - 15 points
    # --------------------------------

    total_images = row["total_images"]

    missing_alt = row["images_without_alt"]

    if total_images == 0:

        score += 10

    else:

        alt_coverage = (
            (total_images - missing_alt)
            / total_images
        )

        score += round(
            alt_coverage * 15
        )


    # --------------------------------
    # 6. Internal Linking - 15 points
    # --------------------------------

    internal_links = row["internal_links"]

    if internal_links >= 10:

        score += 15

    elif internal_links >= 5:

        score += 10

    elif internal_links > 0:

        score += 5


    # --------------------------------
    # 7. External Links - 10 points
    # --------------------------------

    external_links = row["external_links"]

    if external_links >= 3:

        score += 10

    elif external_links > 0:

        score += 5


    # --------------------------------
    # Final Score
    # --------------------------------

    score = min(
        round(score),
        100
    )

    return score


def analyze_dataset(file_path):

    df = pd.read_csv(file_path)

    df["seo_score"] = df.apply(
        calculate_seo_score,
        axis=1
    )

    return df