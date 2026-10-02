import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def analyze_website(url):

    # Add https:// if the user doesn't provide it
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(f"\nAnalyzing: {url}")
    print("-" * 50)

    try:

        # Request the website
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        # Read website HTML
        soup = BeautifulSoup(response.text, "lxml")

        # -----------------------------
        # Page Title
        # -----------------------------

        title = ""

        if soup.title:
            title = soup.title.get_text(strip=True)

        # -----------------------------
        # Meta Description
        # -----------------------------

        meta_description = ""

        meta_tag = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        if meta_tag:
            meta_description = meta_tag.get("content", "")

        # -----------------------------
        # Headings
        # -----------------------------

        h1_tags = soup.find_all("h1")
        h2_tags = soup.find_all("h2")

        h1_count = len(h1_tags)
        h2_count = len(h2_tags)

        # -----------------------------
        # Links
        # -----------------------------

        links = soup.find_all("a", href=True)

        internal_links = 0
        external_links = 0

        website_domain = urlparse(url).netloc

        for link in links:

            href = link.get("href")

            full_url = urljoin(url, href)

            link_domain = urlparse(full_url).netloc

            if link_domain == website_domain:
                internal_links += 1
            else:
                external_links += 1

        # -----------------------------
        # Images
        # -----------------------------

        images = soup.find_all("img")

        images_without_alt = 0

        for image in images:

            alt = image.get("alt")

            if not alt or not alt.strip():
                images_without_alt += 1

        # -----------------------------
        # HTTPS
        # -----------------------------

        https_enabled = url.startswith("https://")

        # -----------------------------
        # Create data dictionary
        # -----------------------------

        website_data = {

            "url": url,

            "status_code": response.status_code,

            "title": title,

            "meta_description": meta_description,

            "h1_count": h1_count,

            "h2_count": h2_count,

            "total_links": len(links),

            "internal_links": internal_links,

            "external_links": external_links,

            "total_images": len(images),

            "images_without_alt": images_without_alt,

            "https_enabled": https_enabled
        }

        return website_data

    except requests.exceptions.RequestException as error:

        print("Could not access the website.")

        print("Error:", error)

        return None