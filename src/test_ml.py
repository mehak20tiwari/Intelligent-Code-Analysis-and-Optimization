import joblib

# Load trained model
model = joblib.load("bug_predictor.pkl")

# Test cases: [lines, loops, conditions]
tests = [
    [6, 1, 0],   # simple code
    [50, 4, 3],  # complex code
    [10, 0, 0],  # very safe code
    [40, 3, 4]   # risky code
]

for features in tests:
    prediction = model.predict([features])[0]
    print(f"Features {features} →", "BUG-PRONE" if prediction else "SAFE")
