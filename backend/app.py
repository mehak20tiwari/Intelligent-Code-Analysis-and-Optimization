from flask import Flask, request, jsonify
from flask_cors import CORS

from ast_analyzer import analyze_code_string
from optimizer_engine import generate_variants, explain_optimization

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    code = request.json.get("code", "")

    analysis = analyze_code_string(code)[0]

    # No executable code → no optimizations
    if analysis["complexity"] == 0:
        return jsonify({
            "analysis": analysis,
            "optimizations": None
        })

    variants = generate_variants(code, analysis)

    explanation = explain_optimization(analysis, variants)

    return jsonify({
        "analysis": analysis,
        "optimizations": {
            "variants": variants,
            "explanation": explanation
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
