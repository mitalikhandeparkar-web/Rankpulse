import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px


# --------------------------------
# Add Project Root to Python Path
# --------------------------------

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


# --------------------------------
# Import Project Modules
# --------------------------------

from src.seo_analysis import calculate_seo_score

from src.seo_issues import find_seo_issues
from src.action_plan import generate_action_plan
from src.ai_explanation import generate_explanation
from src.crawler import analyze_website
from src.competitor_discovery import discover_competitors
from src.competitor_scoring import score_competitors


# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="SEO Insight Engine",
    page_icon="📊",
    layout="wide"
)


# --------------------------------
# Title
# --------------------------------

st.title("📊 SEO Insight Engine")

st.write(
    "Data-driven SEO analysis and opportunity detection"
)


# --------------------------------
# LIVE WEBSITE INPUT
# --------------------------------

st.subheader("🌐 Live Website Analysis")

st.write(
    "Enter a website URL to analyze its SEO performance."
)

url = st.text_input(
    "Website URL",
    placeholder="https://example.com"
)

analyze_button = st.button(
    "🔍 Analyze Website",
    type="primary"
)


# --------------------------------
# Check Website Input
# --------------------------------

if analyze_button:

    if not url.strip():

        st.warning(
            "Please enter a website URL."
        )

        st.stop()


    # --------------------------------
    # Analyze Website
    # --------------------------------

    with st.spinner(
        "Analyzing website... Please wait."
    ):

        result = analyze_website(url)


    # --------------------------------
    # Check Result
    # --------------------------------

    if result is None:

        st.error(
            "Could not analyze this website. "
            "Please check the URL and try again."
        )

        st.stop()


    # --------------------------------
    # Create DataFrame from Live Data
    # --------------------------------

    website_df = pd.DataFrame(
        [result]
    )


    # --------------------------------
    # Calculate SEO Score
    # --------------------------------

    website_df["seo_score"] = website_df.apply(
        calculate_seo_score,
        axis=1
    )


    st.success(
        "Website analyzed successfully!"
    )

else:

    st.info(
        "Enter a website URL above and click "
        "'Analyze Website' to begin."
    )

    st.stop()


# --------------------------------
# Website Information
# --------------------------------

website = website_df.iloc[0]

seo_score = website["seo_score"]


# ==========================================
# LIVE COMPETITOR ANALYSIS
# ==========================================

st.subheader(
    "🏢 Automatically Discovered Competitors"
)

st.write(
    "Competitors are automatically discovered "
    "using live ranking data and analyzed by "
    "the project's SEO scoring system."
)


with st.spinner(
    "Finding and analyzing competitors..."
):

    try:

        competitors = discover_competitors(
            website["url"],
            location_name="India",
            language_name="English",
            limit=100
        )


        if competitors:

            competitor_df = score_competitors(
                competitors
            )

        else:

            competitor_df = pd.DataFrame()


    except Exception as error:

        competitor_df = pd.DataFrame()

        st.warning(
            f"Could not retrieve competitors: {error}"
        )


# --------------------------------
# Temporary Keyword Analysis
# --------------------------------
# This will be replaced with live
# DataForSEO keyword data next.


# ==========================================
# WEBSITE OVERVIEW
# ==========================================

st.subheader(
    "🌐 Website Overview"
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "SEO Score",
        f"{seo_score}/100"
    )


with col2:

    st.metric(
        "H1 Count",
        website["h1_count"]
    )


with col3:

    st.metric(
        "Total Links",
        website["total_links"]
    )


with col4:

    st.metric(
        "Images",
        website["total_images"]
    )


st.write(
    "**Website:**",
    website["url"]
)


# ==========================================
# LIVE WEBSITE DETAILS
# ==========================================

st.subheader(
    "📋 Live Website Details"
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Internal Links",
        website["internal_links"]
    )


with col2:

    st.metric(
        "External Links",
        website["external_links"]
    )


with col3:

    st.metric(
        "Missing ALT",
        website["images_without_alt"]
    )


with col4:

    if website["https_enabled"]:

        st.success(
            "HTTPS Enabled"
        )

    else:

        st.error(
            "HTTPS Not Enabled"
        )


# ==========================================
# SEO DIAGNOSTIC REPORT
# ==========================================

st.subheader(
    "🩺 SEO Diagnostic Report"
)

issues, strengths = find_seo_issues(
    website
)

col1, col2 = st.columns(2)


with col1:

    st.write(
        "### ❌ SEO Problems"
    )

    if issues:

        for issue in issues:

            st.error(issue)

    else:

        st.success(
            "No major SEO problems detected."
        )


with col2:

    st.write(
        "### ✅ SEO Strengths"
    )

    if strengths:

        for strength in strengths:

            st.success(strength)

    else:

        st.info(
            "No strengths detected."
        )


# ==========================================
# LIVE COMPETITOR COMPARISON
# ==========================================

if not competitor_df.empty:

    st.subheader(
        "📊 Live Competitor Comparison"
    )


    # Add analyzed website
    your_website_data = pd.DataFrame(
        [
            {
                "website": website["url"],
                "seo_score": seo_score
            }
        ]
    )


    comparison_df = pd.concat(
        [
            your_website_data,
            competitor_df[
                [
                    "website",
                    "seo_score"
                ]
            ]
        ],
        ignore_index=True
    )


    # --------------------------------
    # Competitor Chart
    # --------------------------------

    fig_competitor = px.bar(
        comparison_df,
        x="website",
        y="seo_score",
        title="Live SEO Score Comparison",
        labels={
            "website": "Website",
            "seo_score": "SEO Score"
        }
    )


    fig_competitor.update_yaxes(
        range=[0, 100]
    )


    st.plotly_chart(
        fig_competitor,
        use_container_width=True
    )


    # --------------------------------
    # Competitor Table
    # --------------------------------

    st.dataframe(
        comparison_df[
            [
                "website",
                "seo_score"
            ]
        ],
        use_container_width=True
    )


else:

    st.info(
        "No competitors were found or analyzed."
    )


# ==========================================
# WHAT-IF SEO SIMULATOR
# ==========================================

st.subheader(
    "🧪 What-If SEO Simulator"
)

st.write(
    "Simulate how fixing SEO issues could change "
    "the project's custom SEO Health Score."
)


current_score = int(
    seo_score
)

simulated_data = website.copy()


fix_title = st.checkbox(
    "Fix page title"
)

fix_meta = st.checkbox(
    "Fix meta description"
)

fix_h1 = st.checkbox(
    "Fix H1 structure"
)

fix_alt = st.checkbox(
    "Fix missing image ALT text"
)

fix_https = st.checkbox(
    "Enable HTTPS"
)

fix_links = st.checkbox(
    "Improve internal linking"
)


# --------------------------------
# Apply Improvements
# --------------------------------

if fix_title:

    simulated_data["title"] = (
        "Optimized SEO Page Title"
    )


if fix_meta:

    simulated_data["meta_description"] = (
        "Optimized meta description for the webpage."
    )


if fix_h1:

    simulated_data["h1_count"] = 1


if fix_alt:

    simulated_data["images_without_alt"] = 0


if fix_https:

    simulated_data["https_enabled"] = True


if fix_links:

    simulated_data["internal_links"] = max(
        int(
            simulated_data["internal_links"]
        ),
        10
    )


# --------------------------------
# Calculate Scenario Score
# --------------------------------

scenario_score = calculate_seo_score(
    simulated_data
)

score_change = (
    scenario_score -
    current_score
)


# --------------------------------
# Display Simulation Results
# --------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Current Score",
        f"{current_score}/100"
    )


with col2:

    st.metric(
        "Scenario Score",
        f"{scenario_score}/100"
    )


with col3:

    st.metric(
        "Estimated Change",
        f"{score_change:+d}"
    )


if score_change > 0:

    st.success(
        "The selected improvements increase "
        "the custom SEO Health Score in this scenario."
    )

elif score_change == 0:

    st.info(
        "The selected improvements do not change "
        "the custom score under the current scoring rules."
    )

else:

    st.warning(
        "The selected scenario results in a lower "
        "custom score."
    )


st.caption(
    "Note: This is a scenario estimate based on "
    "the project's scoring model. It does not "
    "predict Google rankings."
)


# ==========================================
# 30-DAY ACTION PLAN
# ==========================================

st.subheader(
    "📅 30-Day SEO Action Plan"
)

explanations = generate_explanation(
    
    seo_score,
    issues,
    None,
    competitor_df
)


if action_plan:

    for index, action in enumerate(
        action_plan,
        start=1
    ):

        st.markdown(
            f"### {index}. {action['action']}"
        )

        st.write(
            f"**Priority:** {action['priority']}"
        )

        st.write(
            f"**Timeline:** {action['timeline']}"
        )

        st.write(
            f"**Why:** {action['reason']}"
        )

        st.divider()

else:

    st.success(
        "No immediate SEO actions detected."
    )


# ==========================================
# AI-ASSISTED EXPLANATION
# ==========================================

st.subheader(
    "🤖 AI-Assisted SEO Explanation"
)


explanations = generate_explanation(
    seo_score,
    issues,
    keyword_df,
    competitor_df
)


for explanation in explanations:

    st.info(
        explanation
    )


st.caption(
    "This explanation layer summarizes the "
    "analytical results. It does not replace "
    "the underlying data analysis."
)