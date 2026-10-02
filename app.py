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

    data = request.get_json()

    website_url = data.get("url", "").strip()

    if not website_url:
        return jsonify({
            "error": "Website URL is required"
        }), 400

    try:

        # -------------------------
        # 1. Website Analysis
        # -------------------------

        website_data = analyze_website(website_url)

        if website_data is None:
            return jsonify({
                "error": "Could not analyze website"
            }), 400

        seo_score = calculate_seo_score(
            website_data
        )

        issues, strengths = find_seo_issues(
            website_data
        )

        # -------------------------
        # 2. Competitor Discovery
        # -------------------------

        competitors = discover_competitors(
            website_url,
            location_name="India",
            language_name="English",
            limit=50
        )

        # -------------------------
        # 3. Competitor Scoring
        # -------------------------

        competitor_df = score_competitors(
            competitors
        )

        competitor_results = []

        if not competitor_df.empty:

            competitor_results = (
                competitor_df
                .fillna("")
                .to_dict(orient="records")
            )

        # -------------------------
        # Final Response
        # -------------------------

        return jsonify({

            "website": website_data,

            "seo_score": seo_score,

            "issues": issues,

            "strengths": strengths,

            "competitors": competitor_results

        })

    except Exception as error:

        print("ERROR:", error)

        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)