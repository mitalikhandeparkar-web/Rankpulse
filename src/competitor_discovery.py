
import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


EXCLUDED_DOMAINS = {
    "google.com",
    "youtube.com",
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "wikipedia.org",
    "amazon.com",
    "reddit.com",
    "pinterest.com",
    "x.com",
    "twitter.com"
}


load_dotenv(override=True)


def normalize_domain(url):

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def discover_competitors(
    website_url,
    location_name="India",
    language_name="English",
    limit=5
):

    login = os.getenv("DATAFORSEO_LOGIN", "").strip()
    password = os.getenv("DATAFORSEO_PASSWORD", "").strip()

    if not login or not password:
        raise ValueError(
            "DataForSEO credentials not found in .env"
        )

    target_domain = normalize_domain(website_url)

    url = (
        "https://api.dataforseo.com/"
        "v3/dataforseo_labs/google/"
        "competitors_domain/live"
    )

    payload = [
        {
            "target": target_domain,
            "location_name": location_name,
            "language_name": language_name,
            "limit": limit,
            "exclude_top_domains": True
        }
    ]

    response = requests.post(
        url,
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
                "DataForSEO request failed."
            )
        )

    tasks = data.get("tasks", [])

    if not tasks:
        return []

    task = tasks[0]

    if task.get("status_code") != 20000:
        raise RuntimeError(
            task.get(
                "status_message",
                "Competitor discovery failed."
            )
        )

    results = task.get("result", [])

    if not results:
        return []

    items = results[0].get("items", [])

    competitors = []

    for item in items:

        domain = item.get("domain")

        if not domain:
            continue

        if domain.lower() in EXCLUDED_DOMAINS:
            continue

        competitors.append({
            "website": domain,
            "avg_position": item.get("avg_position"),
            "intersections": item.get("intersections")
        })

    return competitors
