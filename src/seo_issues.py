def find_seo_issues(row):

    issues = []
    strengths = []

    # -----------------------------
    # Title
    # -----------------------------

    title = str(row["title"]).strip()

    if not title:
        issues.append("Missing page title")
    else:
        strengths.append("Page title exists")

    # -----------------------------
    # Meta Description
    # -----------------------------

    meta = str(row["meta_description"]).strip()

    if not meta:
        issues.append("Missing meta description")
    else:
        strengths.append("Meta description exists")

    # -----------------------------
    # H1
    # -----------------------------

    if row["h1_count"] == 0:
        issues.append("No H1 heading found")

    elif row["h1_count"] > 1:
        issues.append("Multiple H1 headings found")

    else:
        strengths.append("Exactly one H1 heading found")

    # -----------------------------
    # Images ALT
    # -----------------------------

    total_images = row["total_images"]
    missing_alt = row["images_without_alt"]

    if total_images > 0 and missing_alt > 0:

        issues.append(
            f"{missing_alt} image(s) missing ALT text"
        )

    elif total_images > 0:

        strengths.append(
            "All images have ALT text"
        )

    # -----------------------------
    # HTTPS
    # -----------------------------

    if row["https_enabled"]:

        strengths.append("HTTPS is enabled")

    else:

        issues.append("HTTPS is not enabled")

    # -----------------------------
    # Links
    # -----------------------------

    if row["total_links"] == 0:

        issues.append("No links found")

    else:

        strengths.append(
            f"{row['total_links']} links found"
        )

    return issues, strengths