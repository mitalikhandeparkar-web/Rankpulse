import os
import requests
import pandas as pd
from urllib.parse import urlparse
from dotenv import load_dotenv


load_dotenv(override=True)


def normalize_domain(url):

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    domain = urlparse(url).netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def get_live_keywords(
    website_url,
    location_name="India",
    language_name="English",
    limit=20
):

    login = os.getenv(
        "DATAFORSEO_LOGIN",
        ""
    ).strip()

    password = os.getenv(
        "DATAFORSEO_PASSWORD",
        ""
    ).strip()

    if not login or not password:
        raise ValueError(
            "DataForSEO credentials not found."
        )

    domain = normalize_domain(
        website_url
    )

    api_url = (
        "https://api.dataforseo.com/"
        "v3/dataforseo_labs/google/"
        "ranked_keywords/live"
    )

    payload = [
        {
            "target": domain,
            "location_name": location_name,
            "language_name": language_name,
            "item_types": ["organic"],
            "limit": limit
        }
    ]

    response = requests.post(
        api_url,
        auth=(login, password),
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if data.get("status_code") != 20000:
        raise RuntimeError(
            data.get(
                "status_message",
                "Keyword API request failed."
            )
        )

    tasks = data.get("tasks", [])

    if not tasks:
        return pd.DataFrame()

    task = tasks[0]

    if task.get("status_code") != 20000:
        raise RuntimeError(
            task.get(
                "status_message",
                "Keyword task failed."
            )
        )

    results = task.get(
        "result",
        []
    )

    if not results:
        return pd.DataFrame()

    items = results[0].get(
        "items",
        []
    )

    rows = []

    for item in items:

        keyword_data = item.get(
            "keyword_data",
            {}
        )

        keyword_info = keyword_data.get(
            "keyword_info",
            {}
        )

        ranked_element = item.get(
            "ranked_serp_element",
            {}
        )

        serp_item = ranked_element.get(
            "serp_item",
            {}
        )

        keyword = keyword_data.get(
            "keyword"
        )

        search_volume = keyword_info.get(
            "search_volume",
            0
        )

        position = serp_item.get(
            "rank_absolute"
        )

        difficulty = keyword_info.get(
            "competition_index"
        )

        if keyword and position is not None:

            rows.append({
                "keyword": keyword,
                "search_volume": search_volume or 0,
                "difficulty": difficulty or 0,
                "your_position": position
            })

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    return df