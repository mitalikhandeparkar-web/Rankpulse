def generate_explanation(
    seo_score,
    issues,
    keyword_df,
    competitor_df
):

    explanation = []

    # --------------------------------
    # Overall SEO Health
    # --------------------------------

    if seo_score >= 80:

        explanation.append(
            "The website has a relatively strong technical SEO "
            "foundation based on the project's scoring model."
        )

    elif seo_score >= 60:

        explanation.append(
            "The website has a moderate SEO foundation, "
            "but several areas could be improved."
        )

    else:

        explanation.append(
            "The website has several SEO areas that require "
            "attention based on the project's scoring model."
        )


    # --------------------------------
    # SEO Issues
    # --------------------------------

    if issues:

        explanation.append(
            f"The analysis detected {len(issues)} "
            "SEO issue(s) that should be reviewed."
        )

    # --------------------------------
    # Keyword Opportunities
    # --------------------------------

    if not keyword_df.empty:

        top_keyword = keyword_df.iloc[0]

        explanation.append(
            f"The highest-scoring keyword opportunity is "
            f"'{top_keyword['keyword']}', with an opportunity "
            f"score of {top_keyword['opportunity_score']}."
        )

    # --------------------------------
    # Competitor Comparison
    # --------------------------------

    if len(competitor_df) > 1:

        your_score = competitor_df.iloc[0]["seo_score"]

        best_competitor = competitor_df[
            "seo_score"
        ].max()

        if best_competitor > your_score:

            explanation.append(
                f"The competitor dataset contains websites "
                f"with higher SEO scores than the current "
                f"website, indicating areas for further analysis."
            )

    return explanation