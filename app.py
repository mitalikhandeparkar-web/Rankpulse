from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from src.crawler import analyze_website
from src.seo_analysis import calculate_seo_score
from src.seo_issues import find_seo_issues
from src.competitor_discovery import discover_competitors
from src.competitor_scoring import score_competitors


app = Flask(
    __name__,
    static_folder="frontend",
    static_url_path=""
)

CORS(app)


@app.route("/")
def home():
    return send_from_directory(
        "frontend",
        "index.html"
    )


@app.route("/api/analyze", methods=["POST"])
def analyze():

    data = request.get_json(silent=True) or {}

    website_url = data.get("url", "").strip()

    if not website_url:
        return jsonify({
            "error": "Website URL is required"
        }), 400

    try:

        # =====================================
        # 1. WEBSITE ANALYSIS
        # =====================================

        website_data = analyze_website(
            website_url
        )

        if website_data is None:
            return jsonify({
                "error": "Could not access the website"
            }), 400

        seo_score = calculate_seo_score(
            website_data
        )

        issues, strengths = find_seo_issues(
            website_data
        )


        # =====================================
        # 2. COMPETITOR ANALYSIS
        # =====================================

        competitor_results = []
        competitor_error = None

        try:

            print("Starting competitor discovery...")

            competitors = discover_competitors(
                website_url,
                location_name="India",
                language_name="English",
                limit=3
            )

            print(
                f"Competitors discovered: {len(competitors)}"
            )

            if competitors:

                competitor_df = score_competitors(
                    competitors
                )

                if not competitor_df.empty:

                    competitor_results = (
                        competitor_df
                        .fillna("")
                        .to_dict(
                            orient="records"
                        )
                    )

        except Exception as error:

            print(
                "Competitor analysis error:",
                repr(error)
            )

            competitor_error = (
                "Competitor analysis is "
                "currently unavailable."
            )


        # =====================================
        # 3. FINAL RESPONSE
        # =====================================

        return jsonify({

            "website": website_data,

            "seo_score": seo_score,

            "issues": issues,

            "strengths": strengths,

            "competitors": competitor_results,

            "competitor_error": competitor_error

        })


    except Exception as error:

        print(
            "MAIN ANALYSIS ERROR:",
            repr(error)
        )

        return jsonify({
            "error": "Could not analyze website."
        }), 500


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )