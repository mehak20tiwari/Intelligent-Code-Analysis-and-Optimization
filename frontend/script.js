let variants = [];

/**
 * Main entry point when user clicks "Analyze Code"
 */
async function analyzeCode() {
  const code = document.getElementById("codeInput").value;

  // 🔹 CLEAR PREVIOUS UI STATE (CRITICAL FIX)
  clearOptimizationUI();

  try {
    const response = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code })
    });

    const data = await response.json();

    // ---------------------------
    // ANALYSIS SUMMARY
    // ---------------------------
    document.getElementById("complexity").innerText = data.analysis.complexity;
    document.getElementById("risk").innerText = data.analysis.risk;
    document.getElementById("loops").innerText = data.analysis.loops;
    document.getElementById("conditions").innerText = data.analysis.conditions;

    // ---------------------------
    // ISSUES & INSIGHTS
    // ---------------------------
    const issues = document.getElementById("issues");
    issues.innerHTML = "";

    if (data.analysis.reasons.length === 0) {
      const li = document.createElement("li");
      li.innerText = "No issues detected";
      issues.appendChild(li);
    } else {
      data.analysis.reasons.forEach(reason => {
        const li = document.createElement("li");
        li.innerText = reason;
        issues.appendChild(li);
      });
    }

    // ---------------------------
    // OPTIMIZATION HANDLING
    // ---------------------------

    // 🚨 No executable code → stop here
    if (!data.optimizations) {
      document.getElementById("optimizedCode").innerText =
        "// No executable code to optimize";
      document.getElementById("explanation").innerText =
        "No executable code detected. Optimization is not applicable.";
      return;
    }

    // Store variants
    variants = data.optimizations.variants || [];

    // Explanation
    document.getElementById("explanation").innerText =
      data.optimizations.explanation || "";

    // Show optimized code if available
    if (variants.length > 0) {
      activateTab(0);
      showVariant(0);
    } else {
      document.getElementById("optimizedCode").innerText =
        "// No optimization needed";
    }

  } catch (error) {
    console.error("Error:", error);
    document.getElementById("explanation").innerText =
      "Backend not reachable or error occurred.";
  }
}

/**
 * Clears optimization UI so old results never leak
 */
function clearOptimizationUI() {
  variants = [];

  document.getElementById("optimizedCode").innerText = "";
  document.getElementById("explanation").innerText = "";

  document.querySelectorAll(".tab").forEach(tab => {
    tab.classList.remove("active");
  });
}

/**
 * Switch optimization tabs
 */
function switchTab(index) {
  if (variants.length === 0) return;
  activateTab(index);
  showVariant(index);
}

/**
 * Activate selected tab
 */
function activateTab(index) {
  const tabs = document.querySelectorAll(".tab");
  tabs.forEach(tab => tab.classList.remove("active"));
  if (tabs[index]) tabs[index].classList.add("active");
}

/**
 * Display selected optimized code variant
 */
function showVariant(index) {
  if (!variants[index]) return;
  document.getElementById("optimizedCode").innerText = variants[index][1];
}
