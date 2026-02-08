import ast
import os

# -----------------------------
# FUNCTION-LEVEL ANALYZER
# -----------------------------

class FunctionAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.current_function = None
        self.current_depth = 0

    def visit_FunctionDef(self, node):
        self.current_function = {
            "name": node.name,
            "loops": 0,
            "conditions": 0,
            "max_depth": 0,
            "recursive": False,
            "complexity": 1,
            "reasons": []
        }

        self.current_depth = 0
        self.generic_visit(node)
        self.functions.append(self.current_function)
        self.current_function = None

    def visit_For(self, node):
        if self.current_function:
            self.current_function["loops"] += 1
            self.current_function["complexity"] += 1
            self.current_function["reasons"].append("Contains loop")
        self._enter_block(node)

    def visit_While(self, node):
        if self.current_function:
            self.current_function["loops"] += 1
            self.current_function["complexity"] += 1
            self.current_function["reasons"].append("Contains loop")
        self._enter_block(node)

    def visit_If(self, node):
        if self.current_function:
            self.current_function["conditions"] += 1
            self.current_function["complexity"] += 1
            self.current_function["reasons"].append("Contains conditional logic")
        self._enter_block(node)

    def visit_Call(self, node):
        if (
            self.current_function
            and isinstance(node.func, ast.Name)
            and node.func.id == self.current_function["name"]
        ):
            self.current_function["recursive"] = True
            self.current_function["complexity"] += 1
            self.current_function["reasons"].append("Recursive call")

        self.generic_visit(node)

    def _enter_block(self, node):
        self.current_depth += 1

        if self.current_function:
            self.current_function["max_depth"] = max(
                self.current_function["max_depth"],
                self.current_depth
            )

        self.generic_visit(node)
        self.current_depth -= 1


# -----------------------------
# GLOBAL / RANDOM CODE ANALYZER
# -----------------------------

class BlockAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.loops = 0
        self.conditions = 0
        self.max_depth = 0
        self.current_depth = 0
        self.complexity = 1
        self.reasons = []

    def visit_For(self, node):
        self.loops += 1
        self.complexity += 1
        self.reasons.append("Contains loop")
        self._enter(node)

    def visit_While(self, node):
        self.loops += 1
        self.complexity += 1
        self.reasons.append("Contains loop")
        self._enter(node)

    def visit_If(self, node):
        self.conditions += 1
        self.complexity += 1
        self.reasons.append("Contains conditional logic")
        self._enter(node)

    def _enter(self, node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1


# -----------------------------
# PUBLIC ANALYSIS FUNCTIONS
# -----------------------------

def analyze_file(filepath):
    with open(filepath, "r") as f:
        tree = ast.parse(f.read())

    analyzer = FunctionAnalyzer()
    analyzer.visit(tree)
    return analyzer.functions


def analyze_project(folder="codes"):
    results = []

    for filename in os.listdir(folder):
        if filename.endswith(".py"):
            funcs = analyze_file(os.path.join(folder, filename))
            for f in funcs:
                f["file"] = filename
                results.append(f)

    return results


def analyze_code_string(code):
    tree = ast.parse(code)

    # Try function-level analysis first
    analyzer = FunctionAnalyzer()
    analyzer.visit(tree)

    if analyzer.functions:
        return analyzer.functions

    # Fallback: global code analysis
    block = BlockAnalyzer()
    block.visit(tree)

    return [{
        "name": "GLOBAL_CODE_BLOCK",
        "file": "User_Input_Code",
        "loops": block.loops,
        "conditions": block.conditions,
        "max_depth": block.max_depth,
        "recursive": False,
        "complexity": block.complexity,
        "reasons": block.reasons
    }]
def suggest_optimized_code(code, analysis):
    suggestions = []
    optimized_code = code

    # Rule 1: Loop + even condition optimization
    if (
        analysis["loops"] > 0
        and analysis["conditions"] > 0
        and "% 2 == 0" in code
        and "range" in code
    ):
        suggestions.append(
            "Loop and conditional can be merged using step size in range()"
        )

        # Simple optimization (pattern-based)
        optimized_code = optimized_code.replace(
            "for i in range(x):\n    if i % 2 == 0:",
            "for i in range(0, x, 2):"
        )

    # Rule 2: Deep nesting warning
    if analysis["max_depth"] >= 3:
        suggestions.append(
            "Deep nesting detected; consider flattening logic or early returns"
        )

    # Rule 3: High complexity warning
    if analysis["complexity"] >= 4:
        suggestions.append(
            "High cyclomatic complexity; consider splitting into smaller functions"
        )

    return suggestions, optimized_code
