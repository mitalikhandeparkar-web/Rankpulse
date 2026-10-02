def generate_action_plan(
    issues,
    keyword_df,
    competitor_df
):

    actions = []

    # --------------------------------
    # Technical SEO Issues
    # --------------------------------

    for issue in issues:

        if "title" in issue.lower():

            actions.append({
                "priority": "High",
                "timeline": "Days 1-3",
                "action": "Fix page title",
                "reason": "A clear page title helps search engines and users understand the page."
            })

        elif "meta description" in issue.lower():

            actions.append({
                "priority": "High",
                "timeline": "Days 1-3",
                "action": "Add or improve meta description",
                "reason": "A relevant meta description can improve search-result presentation."
            })

        elif "h1" in issue.lower():

            actions.append({
                "priority": "High",
                "timeline": "Days 4-7",
                "action": "Fix H1 heading structure",
                "reason": "Use a clear primary heading that represents the page topic."
            })

        elif "alt" in issue.lower():

            actions.append({
                "priority": "Medium",
                "timeline": "Days 4-10",
                "action": "Add descriptive ALT text to images",
                "reason": "ALT text improves image accessibility and provides additional page context."
            })

        elif "https" in issue.lower():

            actions.append({
                "priority": "High",
                "timeline": "Days 1-3",
                "action": "Enable HTTPS",
                "reason": "HTTPS provides a secure connection for website visitors."
            })

        elif "links" in issue.lower():

            actions.append({
                "priority": "Medium",
                "timeline": "Days 7-14",
                "action": "Improve internal linking",
                "reason": "Internal links help users and search engines navigate related content."
            })


    # --------------------------------
    # Keyword Opportunities
    # --------------------------------

    high_opportunities = keyword_df[
        keyword_df["opportunity_level"]
        == "High Opportunity"
    ]

    for _, row in high_opportunities.head(3).iterrows():

        actions.append({
            "priority": "High",
            "timeline": "Days 8-21",
            "action": f"Optimize content for '{row['keyword']}'",
            "reason": (
                f"Opportunity score is {row['opportunity_score']} "
                f"with current position {row['your_position']}."
            )
        })


    # --------------------------------
    # Competitor Gap
    # --------------------------------

    if len(competitor_df) > 1:

        your_score = competitor_df.iloc[0]["seo_score"]

        best_score = competitor_df["seo_score"].max()

        if best_score > your_score:

            actions.append({
                "priority": "Medium",
                "timeline": "Days 15-30",
                "action": "Analyze competitor SEO gaps",
                "reason": (
                    f"Your score is {your_score}, while the highest "
                    f"competitor score in the dataset is {best_score}."
                )
            })


    return actions