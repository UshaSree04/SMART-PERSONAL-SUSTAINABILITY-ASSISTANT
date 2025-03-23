import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load dataset
file_path = r"C:\Users\busha\OneDrive\Desktop\training\simplified_sustainability_dataset.csv"
df = pd.read_csv(file_path)

# Drop unnecessary columns
df = df.drop(columns=["Household ID", "Date"])

# Prepare training data
X = df[["Electricity Usage (kWh)", "Water Usage (Liters)", "Food Waste (kg)"]]
y = df["Carbon Footprint (kg CO₂)"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Save model
model_path = r"C:\Users\busha\OneDrive\Desktop\training\carbon_footprint_model.pkl"
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved successfully!")
