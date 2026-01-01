const form = document.getElementById("predictForm");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const features = Array.from(form.querySelectorAll("input[type='number']")).map(input => parseFloat(input.value));

    // Model choice
    const model_type = document.querySelector('input[name="model_choice"]:checked')?.value || "logistic";

    try {
        const response = await fetch(`http://127.0.0.1:8000/predict?model_type=${model_type}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ features })
        });

        const data = await response.json();

        if (response.ok) {
            const text = data.prediction === 0 ? "Benign" : "Malignant";
            resultDiv.textContent = `Prediction (${data.model_used}): ${text}`;
        } else {
            resultDiv.textContent = `Error: ${data.detail || "Something went wrong"}`;
        }
    } catch (error) {
        resultDiv.textContent = "Error connecting to API";
        console.error(error);
    }
});
