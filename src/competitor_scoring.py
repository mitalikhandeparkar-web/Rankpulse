import pandas as pd
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

from .crawler import analyze_website
from .seo_analysis import calculate_seo_score


# -------------------------
# PERFORMANCE SETTINGS
# -------------------------

BATCH_SIZE = 20
MAX_WORKERS = 5

# In-memory cache
CACHE = {}


def analyze_single_competitor(
    competitor
):

    website = competitor["website"]

    # -------------------------
    # CHECK CACHE
    # -------------------------

    if website in CACHE:

        print(
            f"Using cached result: {website}"
        )

        return CACHE[website]

    print(
        f"Analyzing competitor: {website}"
    )

    try:

        # -------------------------
        # CRAWL WEBSITE
        # -------------------------

        data = analyze_website(
            website
        )

        if data is None:

            print(
                f"Could not crawl: {website}"
            )

            return None

        # -------------------------
        # CALCULATE SEO SCORE
        # -------------------------

        seo_score = calculate_seo_score(
            data
        )

        # -------------------------
        # CREATE RESULT
        # -------------------------

        result = {

            "website": website,

            "seo_score": seo_score,

            # Free discovery does not provide
            # paid keyword-position metrics.
            "avg_position":
                competitor.get(
                    "avg_position",
                    ""
                ),

            "intersections":
                competitor.get(
                    "intersections",
                    ""
                ),

            "h1_count":
                data.get(
                    "h1_count",
                    0
                ),

            "total_links":
                data.get(
                    "total_links",
                    0
                ),

            "total_images":
                data.get(
                    "total_images",
                    0
                ),

            "images_without_alt":
                data.get(
                    "images_without_alt",
                    0
                ),

            "https_enabled":
                data.get(
                    "https_enabled",
                    False
                )
        }

        # -------------------------
        # SAVE TO CACHE
        # -------------------------

        CACHE[website] = result

        print(
            f"Cached result: {website}"
        )

        return result

    except Exception as error:

        print(
            f"Error analyzing "
            f"{website}: {error}"
        )

        return None


def score_competitors(
    competitors
):

    results = []

    total = len(competitors)

    if total == 0:

        return pd.DataFrame()

    # -------------------------
    # BATCH PROCESSING
    # -------------------------

    for start in range(
        0,
        total,
        BATCH_SIZE
    ):

        batch = competitors[
            start:start + BATCH_SIZE
        ]

        batch_number = (
            start // BATCH_SIZE
        ) + 1

        total_batches = (
            (total + BATCH_SIZE - 1)
            // BATCH_SIZE
        )

        print(
            f"\nProcessing batch "
            f"{batch_number}/{total_batches}"
        )

        print(
            f"Competitors: "
            f"{start + 1}-"
            f"{start + len(batch)} "
            f"of {total}"
        )

        # -------------------------
        # PARALLEL PROCESSING
        # -------------------------

        with ThreadPoolExecutor(
            max_workers=MAX_WORKERS
        ) as executor:

            futures = [
                executor.submit(
                    analyze_single_competitor,
                    competitor
                )
                for competitor in batch
            ]

            for future in as_completed(
                futures
            ):

                try:

                    result = future.result()

                    if result is not None:

                        results.append(
                            result
                        )

                except Exception as error:

                    print(
                        f"Worker error: {error}"
                    )

    # -------------------------
    # FINAL DATAFRAME
    # -------------------------

    return pd.DataFrame(
        results
    )
