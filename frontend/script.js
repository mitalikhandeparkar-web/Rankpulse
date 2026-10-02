let competitorChart = null;


async function analyzeWebsite() {

    const url = document
        .getElementById("websiteUrl")
        .value
        .trim();

    const loading = document.getElementById("loading");
    const error = document.getElementById("error");
    const results = document.getElementById("results");


    // -------------------------
    // VALIDATE URL
    // -------------------------

    if (!url) {

        error.textContent =
            "Please enter a website URL.";

        return;
    }


    loading.style.display = "block";
    error.textContent = "";
    results.style.display = "none";


    try {

        // -------------------------
        // SEND REQUEST TO FLASK
        // -------------------------

        const response = await fetch(
            "/api/analyze",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    url: url
                })
            }
        );


        // -------------------------
        // READ SERVER RESPONSE
        // -------------------------

        const text = await response.text();

        console.log(
            "Server status:",
            response.status
        );

        console.log(
            "Server response:",
            text
        );


        // -------------------------
        // CHECK EMPTY RESPONSE
        // -------------------------

        if (!text || text.trim() === "") {

            throw new Error(
                "Server returned an empty response. Please check Render logs."
            );
        }


        // -------------------------
        // CONVERT RESPONSE TO JSON
        // -------------------------

        let data;

        try {

            data = JSON.parse(text);

        } catch (jsonError) {

            console.error(
                "JSON parsing error:",
                jsonError
            );

            throw new Error(
                "Server returned an invalid response: " +
                text.substring(0, 200)
            );
        }


        // -------------------------
        // SERVER ERROR
        // -------------------------

        if (!response.ok) {

            throw new Error(
                data.error ||
                "Analysis failed."
            );
        }


        // -------------------------
        // SEO SCORE
        // -------------------------

        document
            .getElementById("seoScore")
            .textContent =
            data.seo_score + "/100";


        // -------------------------
        // WEBSITE DATA
        // -------------------------

        const website = data.website;


        document
            .getElementById("website")
            .textContent =
            website.url;


        document
            .getElementById("statusCode")
            .textContent =
            website.status_code;


        document
            .getElementById("h1Count")
            .textContent =
            website.h1_count;


        document
            .getElementById("internalLinks")
            .textContent =
            website.internal_links;


        document
            .getElementById("totalImages")
            .textContent =
            website.total_images;


        document
            .getElementById("missingAlt")
            .textContent =
            website.images_without_alt;


        document
            .getElementById("pageTitle")
            .textContent =
            website.title || "Not found";


        document
            .getElementById("metaDescription")
            .textContent =
            website.meta_description ||
            "Not found";


        document
            .getElementById("https")
            .textContent =
            website.https_enabled
                ? "Enabled"
                : "Not Enabled";


        // -------------------------
        // SEO ISSUES
        // -------------------------

        const issuesList =
            document.getElementById(
                "issuesList"
            );

        issuesList.innerHTML = "";


        if (
            data.issues &&
            data.issues.length > 0
        ) {

            data.issues.forEach(
                issue => {

                    const li =
                        document.createElement(
                            "li"
                        );

                    li.textContent = issue;

                    issuesList.appendChild(li);

                }
            );

        } else {

            const li =
                document.createElement(
                    "li"
                );

            li.textContent =
                "No major SEO issues detected.";

            issuesList.appendChild(li);
        }


        // -------------------------
        // SEO STRENGTHS
        // -------------------------

        const strengthsList =
            document.getElementById(
                "strengthsList"
            );

        strengthsList.innerHTML = "";


        if (
            data.strengths &&
            data.strengths.length > 0
        ) {

            data.strengths.forEach(
                strength => {

                    const li =
                        document.createElement(
                            "li"
                        );

                    li.textContent =
                        strength;

                    strengthsList.appendChild(li);

                }
            );

        } else {

            const li =
                document.createElement(
                    "li"
                );

            li.textContent =
                "No specific strengths detected.";

            strengthsList.appendChild(li);
        }


        // -------------------------
        // COMPETITORS
        // -------------------------

        renderCompetitors(
            data.competitors || []
        );


        // -------------------------
        // SHOW RESULTS
        // -------------------------

        results.style.display = "block";


    } catch (err) {

        console.error(
            "Analysis error:",
            err
        );

        error.textContent =
            err.message ||
            "Something went wrong while analyzing the website.";

    } finally {

        loading.style.display = "none";

    }
}


// =====================================================
// COMPETITOR RENDERING
// =====================================================

function renderCompetitors(
    competitors
) {

    const table =
        document.getElementById(
            "competitorTable"
        );


    const competitorCount =
        document.getElementById(
            "competitorCount"
        );


    table.innerHTML = "";


    competitorCount.textContent =
        competitors.length +
        " competitors";


    // -------------------------
    // NO COMPETITORS
    // -------------------------

    if (
        !competitors ||
        competitors.length === 0
    ) {

        table.innerHTML = `
            <tr>
                <td colspan="4">
                    No competitors found.
                </td>
            </tr>
        `;

        return;
    }


    // -------------------------
    // COMPETITOR TABLE
    // -------------------------

    competitors.forEach(
        competitor => {

            const row =
                document.createElement(
                    "tr"
                );


            const website =
                competitor.website || "-";


            const seoScore =
                competitor.seo_score ?? "-";


            const avgPosition =
                competitor.avg_position || "-";


            const intersections =
                competitor.intersections || "-";


            row.innerHTML = `

                <td>
                    ${website}
                </td>

                <td>
                    <strong>
                        ${seoScore}
                    </strong>
                </td>

                <td>
                    ${avgPosition}
                </td>

                <td>
                    ${intersections}
                </td>

            `;


            table.appendChild(row);

        }
    );


    // -------------------------
    // COMPETITOR CHART
    // -------------------------

    const labels =
        competitors.map(
            item =>
                item.website || "Unknown"
        );


    const scores =
        competitors.map(
            item =>
                Number(item.seo_score) || 0
        );


    const ctx =
        document.getElementById(
            "competitorChart"
        );


    if (!ctx) {

        console.warn(
            "Competitor chart canvas not found."
        );

        return;
    }


    // Destroy old chart

    if (competitorChart) {

        competitorChart.destroy();

        competitorChart = null;
    }


    // Create new chart

    competitorChart =
        new Chart(
            ctx,
            {

                type: "bar",

                data: {

                    labels: labels,

                    datasets: [

                        {
                            label:
                                "Competitor SEO Score",

                            data: scores
                        }

                    ]
                },

                options: {

                    responsive: true,

                    scales: {

                        y: {

                            beginAtZero: true,

                            max: 100
                        }
                    }
                }
            }
        );
}