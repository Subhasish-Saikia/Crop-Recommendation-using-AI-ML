import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import CubicSpline
from dtaidistance import dtw
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load data from CSV file
data = pd.read_csv('recomendation.csv')

# Define x values (N, P, K, pH, Soil Moisture, Humidity, Temperature)
x = np.array([0, 1, 2, 3, 4, 5, 6])  # Assign numerical values
x_labels = ['N', 'P', 'K', 'pH', 'Soil Moisture', 'Humidity', 'Temperature']

# New graph values
new_y = np.array([90, 45, 50, 5.9, 60, 80, 25])
new_soil_data = pd.DataFrame([new_y], columns=['N', 'P', 'K', 'pH', 'Soil Moisture', 'Humidity', 'Temperature'])

# Use Cubic Spline interpolation for smooth curve
cs_new = CubicSpline(x, new_y)
x_interp = np.linspace(x.min(), x.max(), 100)
y_interp_new = cs_new(x_interp)

plt.figure(figsize=(10, 6))

# Plot old graphs
for index, row in data.iterrows():
    crop = row['Crop']
    y = np.array([row['N'], row['P'], row['K'], row['pH'], row['Soil Moisture'], row['Humidity'], row['Temperature']])
    cs = CubicSpline(x, y)
    y_interp = cs(x_interp)
    plt.plot(x_interp, y_interp, label=crop)
    plt.scatter(x, y)

# Plot the new graph
plt.plot(x_interp, y_interp_new, label='New Graph')
plt.scatter(x, new_y)
plt.xticks(x, x_labels)  # Set x-axis tick labels
plt.xlabel('Parameters')
plt.ylabel('Values')
plt.title('New Graph')
plt.legend()
plt.show()

# Calculate similarity with existing graphs
similarities = []
for index, row in data.iterrows():
    crop = row['Crop']
    y = np.array([row['N'], row['P'], row['K'], row['pH'], row['Soil Moisture'], row['Humidity'], row['Temperature']])
    cs = CubicSpline(x, y)
    y_interp = cs(x_interp)
    distance = dtw.distance(y_interp_new, y_interp)  
    similarity = 1 / (1 + distance)  # Convert distance to similarity
    similarities.append((crop, similarity * 100))  # Convert to percentage

# Print similarities
for crop, similarity in similarities:
    print(f'Similarity with {crop}: {similarity:.2f}%')

# Find the most similar graph
most_similar_crop = max(similarities, key=lambda x: x[1])
print(f'Most similar crop: {most_similar_crop[0]} with similarity {most_similar_crop[1]:.2f}%')

# Define features (X) and target (y)
X = data[['N', 'P', 'K', 'pH', 'Soil Moisture', 'Humidity', 'Temperature']]
y = data['Crop']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)
 
# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:")
print(classification_report(y_test, y_pred))

predicted_crop = model.predict(new_soil_data)
print("Predicted Crop:", predicted_crop[0])