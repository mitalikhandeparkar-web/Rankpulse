import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import (
    urlparse,
    parse_qs,
    unquote
)


# ============================================
# FREE AUTOMATIC COMPETITOR DISCOVERY
# ============================================

EXCLUDED_DOMAINS = {
    "google.com",
    "google.co.in",
    "googleusercontent.com",

    # Search engines
    "bing.com",
    "duckduckgo.com",
    "yahoo.com",

    # Social / platforms
    "youtube.com",
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "wikipedia.org",
    "amazon.com",
    "reddit.com",
    "pinterest.com",
    "x.com",
    "twitter.com",
    "tiktok.com",
    "quora.com",
    "medium.com",
    "github.com",

    # Large technology/platform domains
    "microsoft.com",
    "apple.com"
}


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/154.0 Safari/537.36"
)


def normalize_domain(url):

    if not url:
        return ""

    url = url.strip()

    if not url.startswith(
        ("http://", "https://")
    ):
        url = "https://" + url

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def domain_is_excluded(domain):

    domain = normalize_domain(domain)

    if not domain:
        return True

    for excluded in EXCLUDED_DOMAINS:

        if (
            domain == excluded
            or domain.endswith("." + excluded)
        ):
            return True

    return False


def clean_search_url(href):

    if not href:
        return ""

    href = unquote(href)

    # DuckDuckGo redirect links
    if "uddg=" in href:

        try:

            parsed = urlparse(href)

            values = parse_qs(
                parsed.query
            )

            href = values.get(
                "uddg",
                [href]
            )[0]

        except Exception:
            pass

    if not href.startswith(
        ("http://", "https://")
    ):
        return ""

    return href


# ============================================
# DUCKDUCKGO RESULT EXTRACTION
# ============================================

def extract_ddg_results(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    urls = []

    selectors = [
        "a.result-link",
        "a.result__a",
        "a[data-testid='result-title-a']"
    ]

    for selector in selectors:

        for link in soup.select(selector):

            href = clean_search_url(
                link.get("href", "")
            )

            if href:
                urls.append(href)

    return list(
        dict.fromkeys(urls)
    )


# ============================================
# BING RESULT EXTRACTION
# ============================================

def extract_bing_results(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    urls = []

    selectors = [
        "li.b_algo h2 a",
        "li.b_algo a",
        "h2 a"
    ]

    for selector in selectors:

        for link in soup.select(selector):

            href = clean_search_url(
                link.get("href", "")
            )

            if href:
                urls.append(href)

    return list(
        dict.fromkeys(urls)
    )


# ============================================
# DUCKDUCKGO SEARCH
# ============================================

def search_duckduckgo(query):

    try:

        response = requests.get(
            "https://lite.duckduckgo.com/lite/",
            params={
                "q": query
            },
            headers={
                "User-Agent": USER_AGENT
            },
            timeout=15
        )

        response.raise_for_status()

        return extract_ddg_results(
            response.text
        )

    except Exception as error:

        print(
            "DuckDuckGo search error:",
            repr(error)
        )

        return []


# ============================================
# BING SEARCH
# ============================================

def search_bing(query):

    try:

        response = requests.get(
            "https://www.bing.com/search",
            params={
                "q": query,
                "count": 50
            },
            headers={
                "User-Agent": USER_AGENT
            },
            timeout=15
        )

        response.raise_for_status()

        return extract_bing_results(
            response.text
        )

    except Exception as error:

        print(
            "Bing search error:",
            repr(error)
        )

        return []


# ============================================
# GET TARGET WEBSITE TOPICS
# ============================================

def get_website_topics(website_url):

    try:

        response = requests.get(
            website_url,
            headers={
                "User-Agent": USER_AGENT
            },
            timeout=15,
            allow_redirects=True
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # ----------------------------------------
        # Title
        # ----------------------------------------

        title = ""

        if soup.title:

            title = soup.title.get_text(
                " ",
                strip=True
            )

        # ----------------------------------------
        # H1
        # ----------------------------------------

        h1 = ""

        h1_tag = soup.find("h1")

        if h1_tag:

            h1 = h1_tag.get_text(
                " ",
                strip=True
            )

        # ----------------------------------------
        # Meta description
        # ----------------------------------------

        meta_description = ""

        meta = soup.find(
            "meta",
            attrs={
                "name": re.compile(
                    "^description$",
                    re.I
                )
            }
        )

        if meta:

            meta_description = (
                meta.get("content", "")
                .strip()
            )

        return {
            "title": title,
            "h1": h1,
            "description": meta_description
        }

    except Exception as error:

        print(
            "Could not read target topics:",
            repr(error)
        )

        return {
            "title": "",
            "h1": "",
            "description": ""
        }


# ============================================
# CREATE COMPETITOR SEARCH QUERIES
# ============================================

def make_queries(
    website_url,
    topics
):

    target_domain = normalize_domain(
        website_url
    )

    queries = []

    title = topics.get(
        "title",
        ""
    ).strip()

    h1 = topics.get(
        "h1",
        ""
    ).strip()

    description = topics.get(
        "description",
        ""
    ).strip()

    # ========================================
    # Domain based queries
    # ========================================

    if target_domain:

        queries.append(
            f'"{target_domain}" competitors'
        )

        queries.append(
            f'"{target_domain}" alternatives'
        )

    # ========================================
    # Title based query
    # ========================================

    if title:

        clean_title = re.sub(
            r"[^A-Za-z0-9 ]",
            " ",
            title
        ).strip()

        words = clean_title.split()

        if words:

            short_title = " ".join(
                words[:6]
            )

            queries.append(
                f'"{short_title}" competitors'
            )

    # ========================================
    # H1 based query
    # ========================================

    if h1:

        clean_h1 = re.sub(
            r"[^A-Za-z0-9 ]",
            " ",
            h1
        ).strip()

        words = clean_h1.split()

        if words:

            short_h1 = " ".join(
                words[:6]
            )

            queries.append(
                f'"{short_h1}" alternatives'
            )

    # ========================================
    # Description based query
    # ========================================

    if description:

        words = re.findall(
            r"[A-Za-z]{4,}",
            description
        )

        keywords = " ".join(
            words[:8]
        )

        if keywords:

            queries.append(
                f"{keywords} competitors"
            )

    # ========================================
    # Remove duplicate queries
    # ========================================

    final_queries = []

    for query in queries:

        if query not in final_queries:

            final_queries.append(query)

    return final_queries[:5]


# ============================================
# DISCOVER COMPETITORS
# ============================================

def discover_competitors(
    website_url,
    location_name="India",
    language_name="English",
    limit=10
):

    target_domain = normalize_domain(
        website_url
    )

    if not target_domain:
        return []

    # ========================================
    # Read target website
    # ========================================

    topics = get_website_topics(
        website_url
    )

    # ========================================
    # Generate search queries
    # ========================================

    queries = make_queries(
        website_url,
        topics
    )

    print(
        "Generated competitor queries:",
        queries
    )

    candidate_urls = []

    # ========================================
    # SEARCH DUCKDUCKGO
    # ========================================

    for query in queries:

        print(
            "DuckDuckGo competitor search:",
            query
        )

        results = search_duckduckgo(
            query
        )

        print(
            "DuckDuckGo results:",
            len(results)
        )

        candidate_urls.extend(
            results
        )

        if len(candidate_urls) >= limit * 5:
            break

    # ========================================
    # SEARCH BING
    # Always use Bing also to increase coverage
    # ========================================

    if len(candidate_urls) < limit * 5:

        for query in queries:

            print(
                "Bing competitor search:",
                query
            )

            results = search_bing(
                query
            )

            print(
                "Bing results:",
                len(results)
            )

            candidate_urls.extend(
                results
            )

            if len(candidate_urls) >= limit * 5:
                break

    # ========================================
    # REMOVE DUPLICATE SEARCH URLs
    # ========================================

    candidate_urls = list(
        dict.fromkeys(candidate_urls)
    )

    print(
        "Total candidate URLs:",
        len(candidate_urls)
    )

    # ========================================
    # FILTER COMPETITORS
    # ========================================

    competitors = []

    seen_domains = set()

    for url in candidate_urls:

        domain = normalize_domain(
            url
        )

        if not domain:
            continue

        # ------------------------------------
        # Remove target website
        # ------------------------------------

        if domain == target_domain:
            continue

        # ------------------------------------
        # Remove duplicate domains
        # ------------------------------------

        if domain in seen_domains:
            continue

        # ------------------------------------
        # Remove excluded domains
        # ------------------------------------

        if domain_is_excluded(
            domain
        ):
            continue

        seen_domains.add(
            domain
        )

        # ------------------------------------
        # Add competitor
        # ------------------------------------

        competitors.append({
            "website": "https://" + domain,
            "avg_position": "",
            "intersections": ""
        })

        # ------------------------------------
        # Maximum competitors
        # ------------------------------------

        if len(competitors) >= limit:
            break

    # ========================================
    # FINAL OUTPUT
    # ========================================

    print(
        "Potential competitors:",
        competitors
    )

    print(
        "Competitor discovered:",
        len(competitors)
    )

    return competitors