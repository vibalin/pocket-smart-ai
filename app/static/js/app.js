async function sendForm(form, endpoint) {

    const isFileForm =
        form.enctype === "multipart/form-data";

    const body = isFileForm
        ? new FormData(form)
        : new URLSearchParams(
            new FormData(form)
        );

    const response = await fetch(
        endpoint,
        {
            method: "POST",
            body: body
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.error ||
            data.detail ||
            "Something went wrong."
        );
    }

    return data;
}


document.addEventListener(
    "DOMContentLoaded",
    () => {

        const registerForm =
            document.getElementById(
                "registerForm"
            );

        if (registerForm) {

            registerForm.addEventListener(
                "submit",
                async (event) => {

                    event.preventDefault();

                    try {

                        const data =
                            await sendForm(
                                registerForm,
                                "/register"
                            );

                        window.location.href =
                            data.redirect;

                    } catch (error) {

                        document.getElementById(
                            "message"
                        ).textContent =
                            error.message;
                    }
                }
            );
        }


        const loginForm =
            document.getElementById(
                "loginForm"
            );

        if (loginForm) {

            loginForm.addEventListener(
                "submit",
                async (event) => {

                    event.preventDefault();

                    try {

                        const data =
                            await sendForm(
                                loginForm,
                                "/login"
                            );

                        window.location.href =
                            data.redirect;

                    } catch (error) {

                        document.getElementById(
                            "message"
                        ).textContent =
                            error.message;
                    }
                }
            );
        }


        document
            .querySelectorAll(
                ".planner-form"
            )
            .forEach(form => {

                form.addEventListener(
                    "submit",
                    async (event) => {

                        event.preventDefault();

                        const message =
                            document.getElementById(
                                "plannerMessage"
                            );

                        message.textContent =
                            "Generating recommendation...";

                        try {

                            const data =
                                await sendForm(
                                    form,
                                    form.dataset.endpoint
                                );

                            window.location.href =
                                `/recommendation-page/${data.id}`;

                        } catch (error) {

                            message.textContent =
                                error.message;
                        }
                    }
                );
            });


        loadRecommendation();
        loadHistory();
    }
);


async function loadRecommendation() {

    const box =
        document.getElementById(
            "recommendation"
        );

    if (!box) {
        return;
    }

    const id =
        box.dataset.id;

    const response =
        await fetch(
            `/recommendations-details/${id}`
        );

    const data =
        await response.json();

    if (!response.ok) {

        box.innerHTML =
            `<p class="message-error">
                ${escapeHtml(data.error)}
            </p>`;

        return;
    }

    const recommendation =
        data.recommendation;

    let html = `
        <div class="page-heading">

            <p class="eyebrow">
                ${escapeHtml(
                    recommendation.planner
                ).toUpperCase()}
            </p>

            <h1>
                ${escapeHtml(
                    recommendation.title
                )}
            </h1>

            <p>
                ${escapeHtml(
                    recommendation.summary
                )}
            </p>

            <strong>
                Budget:
                ₹${Number(
                    recommendation.budget
                ).toLocaleString()}
            </strong>

            <p>
                Estimated Cost:
                ₹${Number(
                    recommendation.total_estimated_cost
                ).toLocaleString()}
            </p>

        </div>
    `;


    for (
        const product
        of recommendation.products
    ) {

        html += `
            <div class="product">

                <h3>
                    ${escapeHtml(
                        product.name
                    )}
                </h3>

                <p>
                    <b>Category:</b>
                    ${escapeHtml(
                        product.category
                    )}
                </p>

                <p>
                    <b>Estimated Price:</b>
                    ₹${Number(
                        product.estimated_price
                    ).toLocaleString()}
                </p>

                <p>
                    ${escapeHtml(
                        product.reason
                    )}
                </p>

                <a
                    class="btn"
                    target="_blank"
                    href="${product.platform_url}"
                >
                    Search on
                    ${escapeHtml(
                        product.platform
                    )}
                </a>

            </div>
        `;
    }


    html += `
        <div class="card">

            <h3>
                Tips
            </h3>

            <ul>
    `;


    for (
        const tip
        of recommendation.tips || []
    ) {

        html += `
            <li>
                ${escapeHtml(tip)}
            </li>
        `;
    }


    html += `
            </ul>

        </div>
    `;


    box.innerHTML = html;
}


async function loadHistory() {

    const box =
        document.getElementById(
            "historyList"
        );

    if (!box) {
        return;
    }

    const response =
        await fetch("/history");

    const data =
        await response.json();

    if (!response.ok) {

        box.innerHTML =
            `<p class="message-error">
                ${escapeHtml(
                    data.error ||
                    data.detail
                )}
            </p>`;

        return;
    }


    if (data.length === 0) {

        box.innerHTML =
            `<div class="card">
                <p>
                    No recommendations yet.
                </p>
            </div>`;

        return;
    }


    box.innerHTML =
        data.map(item => `

            <div class="history-item">

                <h3>
                    ${escapeHtml(
                        item.planner_type
                    )}
                    planner
                </h3>

                <p>
                    Budget:
                    ₹${Number(
                        item.budget
                    ).toLocaleString()}
                </p>

                <p>
                    ${new Date(
                        item.created_at
                    ).toLocaleString()}
                </p>

                <a
                    class="btn"
                    href="/recommendation-page/${item.id}"
                >
                    View
                </a>

            </div>

        `).join("");
}


function escapeHtml(value) {

    return String(
        value ?? ""
    )
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll(
            '"',
            "&quot;"
        )
        .replaceAll(
            "'",
            "&#039;"
        );
}