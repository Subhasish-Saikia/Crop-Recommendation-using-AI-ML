from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT / "recomendation.csv"
MODEL_PATH = ROOT / "crop_model.pkl"

data = pd.read_csv(DATASET_PATH)

print("\nDataset loaded successfully!")
print("Shape:", data.shape)

print("\nFirst 5 rows:")
print(data.head())

print("\nMissing values:")
print(data.isnull().sum())

print("\nCrop distribution:")
print(data["Crop"].value_counts())

features = [
    "N",
    "P",
    "K",
    "pH",
    "Soil Moisture",
    "Humidity",
    "Temperature"
]

X = data[features]
y = data["Crop"]


# ============================================================
# 4. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    random_state=42,
    n_jobs=-1
)

print("\nTraining model...")

model.fit(X_train, y_train)

print("Training completed!")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n================================")
print("MODEL PERFORMANCE")
print("================================")

print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\n================================")
print("FEATURE IMPORTANCE")
print("================================")

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print(importance)

new_soil_data = pd.DataFrame(
    [[90, 45, 50, 5.9, 60, 80, 25]],
    columns=features
)

predicted_crop = model.predict(new_soil_data)

print("\n================================")
print("CROP RECOMMENDATION")
print("================================")

print("Input:")
print(new_soil_data)

print("\nRecommended Crop:", predicted_crop[0])

probabilities = model.predict_proba(new_soil_data)[0]

results = pd.DataFrame({
    "Crop": model.classes_,
    "Probability": probabilities
})

results = results.sort_values(
    by="Probability",
    ascending=False
)

print("\nCrop probabilities:")

for _, row in results.head(5).iterrows():
    print(
        f"{row['Crop']}: "
        f"{row['Probability'] * 100:.2f}%"
    )
    
joblib.dump(model, MODEL_PATH)

print("\n================================")
print("MODEL SAVED")
print("================================")

print(f"Saved as: {MODEL_PATH}")