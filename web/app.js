(() => {
  "use strict";

  const queryEl = document.getElementById("query");
  const charCountEl = document.getElementById("char-count");
  const analyzeBtn = document.getElementById("analyze-btn");
  const resultEl = document.getElementById("result");
  const errorEl = document.getElementById("error");
  const labelEl = document.getElementById("result-label");
  const vibeEl = document.getElementById("result-vibe");
  const percentEl = document.getElementById("result-percent");
  const meterFillEl = document.getElementById("meter-fill");
  const meterThumbEl = document.getElementById("meter-thumb");

  function updateCharCount() {
    charCountEl.textContent = `${queryEl.value.length} / 4000`;
  }

  function showError(message) {
    errorEl.textContent = message;
    errorEl.classList.remove("hidden");
  }

  function hideError() {
    errorEl.classList.add("hidden");
  }

  function setLoading(loading) {
    analyzeBtn.disabled = loading;
    analyzeBtn.classList.toggle("loading", loading);
    analyzeBtn.querySelector(".btn-label").textContent = loading
      ? "jev is cooking"
      : "run the check";
  }

  function showResult(data) {
    labelEl.textContent = data.label;
    labelEl.classList.remove("glitch");
    void labelEl.offsetWidth;
    labelEl.classList.add("glitch");

    vibeEl.textContent = data.vibe;
    percentEl.textContent = `${data.percent}%`;

    meterFillEl.style.width = `${100 - data.percent}%`;
    meterThumbEl.style.left = `${data.percent}%`;

    resultEl.classList.remove("hidden");
  }

  async function analyze() {
    const text = queryEl.value.trim();
    if (text.length < 3) {
      showError("bestie you gotta paste at least 3 characters 💀");
      return;
    }

    hideError();
    setLoading(true);

    try {
      const response = await fetch(`${window.location.origin}/api/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.detail || "jev said nah — try again");
      }

      showResult(data);
    } catch (error) {
      showError(
        error.message ||
          "connection failed — run `uv run red-flag` in the project folder"
      );
      resultEl.classList.add("hidden");
    } finally {
      setLoading(false);
    }
  }

  queryEl.addEventListener("input", updateCharCount);
  analyzeBtn.addEventListener("click", analyze);
  queryEl.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
      analyze();
    }
  });

  updateCharCount();
})();
