const form = document.getElementById("predictionForm");
const resetBtn = document.getElementById("resetBtn");
const predictBtn = document.getElementById("predictBtn");
const buttonText = document.getElementById("buttonText");
const spinner = document.getElementById("spinner");
const emptyState = document.getElementById("emptyState");
const resultState = document.getElementById("resultState");
const predictionValue = document.getElementById("predictionValue");
const toast = document.getElementById("toast");

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  window.clearTimeout(window.homeValueToastTimer);
  window.homeValueToastTimer = window.setTimeout(() => toast.classList.remove("show"), 3200);
}
function formatEstimate(value) {
  return new Intl.NumberFormat("en-US", {style:"currency", currency:"USD", maximumFractionDigits:0}).format(value);
}
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = Object.fromEntries(new FormData(form).entries());
  predictBtn.disabled = true;
  buttonText.textContent = "Calculating…";
  spinner.classList.remove("hidden");
  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not calculate an estimate.");
    predictionValue.textContent = formatEstimate(data.prediction);
    emptyState.classList.add("hidden");
    resultState.classList.remove("hidden");
  } catch (error) {
    showToast(error.message || "Something went wrong. Please try again.");
  } finally {
    predictBtn.disabled = false;
    buttonText.innerHTML = 'Estimate price <b>↗</b>';
    spinner.classList.add("hidden");
  }
});
resetBtn.addEventListener("click", () => {
  form.reset();
  resultState.classList.add("hidden");
  emptyState.classList.remove("hidden");
});
