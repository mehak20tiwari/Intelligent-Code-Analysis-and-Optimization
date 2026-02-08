import ast

def analyze_code_string(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return [{
            "complexity": 0,
            "loops": 0,
            "conditions": 0,
            "max_depth": 0,
            "risk": "N/A",
            "reasons": ["Syntax error detected"]
        }]

    # Detect executable code
    has_exec = any(
        isinstance(node, (ast.Assign, ast.For, ast.While, ast.If, ast.FunctionDef, ast.Expr))
        for node in ast.walk(tree)
    )

    if not has_exec:
        return [{
            "complexity": 0,
            "loops": 0,
            "conditions": 0,
            "max_depth": 0,
            "risk": "N/A",
            "reasons": ["No executable code detected"]
        }]

    loops = 0
    conditions = 0
    max_depth = 0

    def walk(node, depth=0):
        nonlocal loops, conditions, max_depth
        max_depth = max(max_depth, depth)

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.For, ast.While)):
                loops += 1
                walk(child, depth + 1)
            elif isinstance(child, ast.If):
                conditions += 1
                walk(child, depth + 1)
            else:
                walk(child, depth)

    walk(tree)

    complexity = 1 + loops + conditions

    if complexity <= 2:
        risk = "LOW"
    elif complexity <= 4:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    reasons = []
    if loops:
        reasons.append("Loop logic detected")
    if conditions:
        reasons.append("Conditional branching detected")
    if max_depth > 2:
        reasons.append("Deep nesting increases complexity")

    return [{
        "complexity": complexity,
        "loops": loops,
        "conditions": conditions,
        "max_depth": max_depth,
        "risk": risk,
        "reasons": reasons
    }]
