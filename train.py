import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load dataset
file_path = r"C:\Users\busha\OneDrive\Desktop\training\simplified_sustainability_dataset.csv"
df = pd.read_csv(file_path)

# Drop unnecessary columns
df = df.drop(columns=["Household ID", "Date"])

# Define features (X) and target (y)
X = df[["Electricity Usage (kWh)", "Water Usage (Liters)", "Food Waste (kg)"]]
y = df["Carbon Footprint (kg CO₂)"]

# Split dataset (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on test data
y_pred = model.predict(X_test)

# Evaluate accuracy
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\n📊 Model Evaluation Metrics:")
print(f"📏 Mean Absolute Error (MAE): {mae:.2f}")
print(f"🔢 Mean Squared Error (MSE): {mse:.2f}")
print(f"📉 Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"📊 R² Score: {r2:.4f} (Closer to 1 is better)")

# Save trained model
model_path = r"C:\Users\busha\OneDrive\Desktop\training\carbon_footprint_model.pkl"
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print("\n✅ Model trained and saved successfully!")