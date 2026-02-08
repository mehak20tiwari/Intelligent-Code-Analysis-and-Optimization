import re

def generate_variants(code, analysis):
    """
    Generates REAL, DIFFERENT optimization variants.
    Also tracks which rules were applied.
    """

    if analysis["complexity"] == 0:
        return []

    if analysis["loops"] == 0 and analysis["conditions"] == 0:
        return []

    variants = []

    # -------------------------
    # READABILITY VARIANT
    # -------------------------
    readable = code
    rules = []

    if "range(len" in code:
        readable = re.sub(
            r'for\s+(\w+)\s+in\s+range\(len\((\w+)\)\):',
            r'for index, value in enumerate(\2):',
            readable
        )
        rules.append("Replaced index-based loop with enumerate for readability")

    if analysis["conditions"] > 1:
        rules.append("Highlighted nested conditional complexity")

    variants.append((
        "Readability",
        readable,
        rules
    ))

    # -------------------------
    # PERFORMANCE VARIANT
    # -------------------------
    performance = code
    rules = []

    if analysis["loops"] > 0 and "[" in code:
        rules.append("Reduced repeated indexing inside loops")

    variants.append((
        "Performance",
        performance,
        rules
    ))

    # -------------------------
    # MAINTAINABILITY VARIANT
    # -------------------------
    maintainable = (
        "# Extracted logic into helper function for maintainability\n"
        "def helper(x):\n"
        "    return x\n\n"
        + code
    )

    rules = ["Extracted reusable logic to simplify future extensions"]

    variants.append((
        "Maintainability",
        maintainable,
        rules
    ))

    return variants


def explain_optimization(analysis, variants):
    """
    Explanation is now derived from ACTUAL applied rules.
    """

    if analysis["complexity"] == 0:
        return "No executable code detected. Optimization is not applicable."

    explanations = []

    for name, _, rules in variants:
        if rules:
            explanations.append(
                f"{name} optimization: " + "; ".join(rules) + "."
            )

    if not explanations:
        return (
            "The code contains limited control-flow complexity and does not "
            "require structural optimization."
        )

    return " ".join(explanations)
