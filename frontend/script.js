let competitorChart = null;


async function analyzeWebsite() {

    const url =
        document
        .getElementById("websiteUrl")
        .value
        .trim();


    const loading =
        document.getElementById("loading");

    const error =
        document.getElementById("error");

    const results =
        document.getElementById("results");


    if (!url) {

        error.textContent =
            "Please enter a website URL.";

        return;
    }


    loading.style.display = "block";

    error.textContent = "";

    results.style.display = "none";


    try {

        const response = await fetch(
            "/api/analyze",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    url: url
                })
            }
        );


        const data =
            await response.json();


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

        const website =
            data.website;


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
        // ISSUES
        // -------------------------

        const issuesList =
            document
            .getElementById("issuesList");


        issuesList.innerHTML = "";


        if (
            data.issues &&
            data.issues.length > 0
        ) {

            data.issues.forEach(issue => {

                const li =
                    document.createElement("li");

                li.textContent = issue;

                issuesList.appendChild(li);

            });

        } else {

            const li =
                document.createElement("li");

            li.textContent =
                "No major SEO issues detected.";

            issuesList.appendChild(li);
        }


        // -------------------------
        // STRENGTHS
        // -------------------------

        const strengthsList =
            document
            .getElementById("strengthsList");


        strengthsList.innerHTML = "";


        if (
            data.strengths &&
            data.strengths.length > 0
        ) {

            data.strengths.forEach(strength => {

                const li =
                    document.createElement("li");

                li.textContent = strength;

                strengthsList.appendChild(li);

            });

        }


        // -------------------------
        // COMPETITORS
        // -------------------------

        renderCompetitors(
            data.competitors || []
        );


        results.style.display = "block";


    } catch (err) {

        error.textContent =
            err.message;

    } finally {

        loading.style.display = "none";
    }
}



function renderCompetitors(
    competitors
) {

    const table =
        document
        .getElementById(
            "competitorTable"
        );


    table.innerHTML = "";


    document
        .getElementById(
            "competitorCount"
        )
        .textContent =
        competitors.length +
        " competitors";


    if (competitors.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="4">
                    No competitors found.
                </td>
            </tr>
        `;

        return;
    }


    competitors.forEach(
        competitor => {

            const row =
                document.createElement("tr");


            row.innerHTML = `

                <td>
                    ${competitor.website}
                </td>

                <td>
                    <strong>
                        ${competitor.seo_score}
                    </strong>
                </td>

                <td>
                    ${competitor.avg_position || "-"}
                </td>

                <td>
                    ${competitor.intersections || "-"}
                </td>

            `;


            table.appendChild(row);

        }
    );


    // -------------------------
    // CHART
    // -------------------------

    const labels =
        competitors.map(
            item => item.website
        );


    const scores =
        competitors.map(
            item => item.seo_score
        );


    const ctx =
        document
        .getElementById(
            "competitorChart"
        );


    if (competitorChart) {

        competitorChart.destroy();

    }


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