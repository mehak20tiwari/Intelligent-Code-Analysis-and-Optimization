import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------
# STEP 1: Read all code files
# ---------------------------------
folder_path = "codes"
documents = []
filenames = []

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "r") as file:
        documents.append(file.read())
        filenames.append(filename)

# ---------------------------------
# STEP 2: TF-IDF Search Model
# ---------------------------------
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

# ---------------------------------
# STEP 3: User Search
# ---------------------------------
query = input("Enter search sentence: ").lower()

semantic_map = {
    "loop": "for",
    "loops": "for",
    "function": "def",
    "functions": "def"
}

for word, replacement in semantic_map.items():
    query = query.replace(word, replacement)

query_vector = vectorizer.transform([query])
similarity_scores = cosine_similarity(query_vector, tfidf_matrix)[0]

ranked_results = sorted(
    zip(filenames, documents, similarity_scores),
    key=lambda x: x[2],
    reverse=True
)

# ---------------------------------
# STEP 4: Code Review Functions
# ---------------------------------
def analyze_code(code):
    lines = code.split("\n")
    loc = len(lines)

    loop_count = code.count("for ") + code.count("while ")
    condition_count = code.count("if ") + code.count("elif ")

    # Simple risk scoring
    risk_score = 0
    if loc > 20:
        risk_score += 2
    if loop_count > 1:
        risk_score += 3
    if condition_count > 2:
        risk_score += 2

    return loc, loop_count, condition_count, risk_score

# ---------------------------------
# STEP 5: Show Search + Review
# ---------------------------------
print("\n🔍 Search Results with Code Review:\n")

found = False

for filename, code, score in ranked_results:
    if score > 0:
        loc, loops, conditions, risk = analyze_code(code)

        print(f"📄 File: {filename}")
        print(f"   Relevance Score : {score:.4f}")
        print(f"   Lines of Code   : {loc}")
        print(f"   Loops           : {loops}")
        print(f"   Conditions      : {conditions}")

        if risk >= 5:
            print("   ML Prediction   : HIGH (Bug-prone)")
        elif risk >= 3:
            print("   ML Prediction   : MEDIUM")
        else:
            print("   ML Prediction : SAFE")

        print("-" * 40)
        found = True

if not found:
    print("No relevant files found.")
