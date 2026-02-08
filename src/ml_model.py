import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# --------------------------------
# STEP 1: Create training data
# --------------------------------
data = {
    "lines": [5, 20, 35, 50, 10, 45, 60],
    "loops": [0, 1, 2, 3, 0, 3, 4],
    "conditions": [0, 1, 2, 4, 0, 3, 5],
    "buggy": [0, 0, 1, 1, 0, 1, 1]
}

df = pd.DataFrame(data)

X = df[["lines", "loops", "conditions"]]
y = df["buggy"]

# --------------------------------
# STEP 2: Train/Test split
# --------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# --------------------------------
# STEP 3: Train ML model
# --------------------------------
model = RandomForestClassifier()
model.fit(X_train, y_train)

# --------------------------------
# STEP 4: Evaluate
# --------------------------------
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)

# --------------------------------
# STEP 5: Save model
# --------------------------------
joblib.dump(model, "bug_predictor.pkl")
print("Model saved as bug_predictor.pkl")
