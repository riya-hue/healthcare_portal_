console.log("EL Care loaded");

// SAME FastAPI backend (Railway / Local)
const BACKEND_URL = "";

// Convert form data to JSON
function toJSON(form) {
  const data = {};
  new FormData(form).forEach((v, k) => (data[k] = Number(v)));
  return data;
}

// Submit form data to backend
async function submitForm(form) {
  const resultContainer = document.getElementById("result");
  resultContainer.textContent = "⏳ Analyzing...";

  try {
    const res = await fetch("/analyze_heart", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(toJSON(form)),
    });

    if (!res.ok) {
      throw new Error(`Server error: ${res.status}`);
    }

    const result = await res.json();

    resultContainer.innerHTML = `
      🩺 Heart Disease: <b>${result.heart_disease}</b><br>
      📊 Risk Probability: <b>${result.risk_probability}%</b>
    `;
  } catch (err) {
    console.error(err);
    resultContainer.textContent = "❌ Backend error. Please try again later.";
  }
}

// Attach submit event
document.addEventListener("DOMContentLoaded", () => {
  const heartForm = document.getElementById("heartForm");
  if (heartForm) {
    heartForm.addEventListener("submit", (e) => {
      e.preventDefault();
      submitForm(e.target);
    });
  }
});

