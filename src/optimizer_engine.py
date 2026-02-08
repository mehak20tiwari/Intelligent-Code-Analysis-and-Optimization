import math

# -----------------------------
# ML-like ranking (lightweight)
# -----------------------------

def rank_suggestions(analysis, suggestions):
    """
    Rank optimization suggestions using heuristic ML-style scoring
    """
    scores = []

    for s in suggestions:
        score = 0.0

        # Feature-based scoring
        score += 0.3 * analysis["complexity"]
        score += 0.2 * analysis["max_depth"]
        score += 0.2 * analysis["loops"]
        score += 0.1 * analysis["conditions"]

        if "loop" in s.lower():
            score += 0.2
        if "nest" in s.lower():
            score += 0.15
        if "split" in s.lower():
            score += 0.1

        scores.append((round(min(score, 1.0), 2), s))

    return sorted(scores, reverse=True)


# -----------------------------
# MULTI-VARIANT OPTIMIZATION
# -----------------------------

def generate_variants(code, analysis):
    variants = []

    # Variant 1: Performance
    if "for" in code and "% 2 == 0" in code:
        perf = code.replace(
            "for i in range(x):\n    if i % 2 == 0:",
            "for i in range(0, x, 2):"
        )
        variants.append(("Performance", perf))

    # Variant 2: Readability
    if "for" in code and "% 2 == 0" in code:
        readable = (
            "evens = [i for i in range(x) if i % 2 == 0]\n"
            "for i in evens:\n"
            "    print(i)"
        )
        variants.append(("Readability", readable))

    # Variant 3: Maintainability
    if analysis["complexity"] >= 4:
        maintainable = (
            "# Consider splitting logic into smaller functions\n"
            + code
        )
        variants.append(("Maintainability", maintainable))

    return variants


# -----------------------------
# NATURAL LANGUAGE EXPLANATION
# -----------------------------

def explain_optimization(analysis):
    explanation = []

    explanation.append(
        "The original code contains multiple decision paths, "
        "which increases cyclomatic complexity."
    )

    if analysis["loops"] > 0 and analysis["conditions"] > 0:
        explanation.append(
            "A conditional inside a loop causes repeated checks "
            "for every iteration."
        )

    if analysis["max_depth"] >= 3:
        explanation.append(
            "Deep nesting reduces readability and makes debugging harder."
        )

    explanation.append(
        "The optimized versions reduce unnecessary checks "
        "and simplify control flow."
    )

    return " ".join(explanation)
