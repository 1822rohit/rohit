import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# ------------------------
# Sample dataset (Pune city house prices)
# ------------------------
data = {
    'location': ['Kothrud', 'Hinjewadi', 'Viman Nagar', 'Baner', 'Koregaon Park', 'Kothrud', 'Baner', 'Hinjewadi'],
    'bhk': [2, 3, 2, 3, 4, 1, 2, 2],
    'sqft': [1000, 1500, 1200, 1600, 2500, 800, 1100, 1300],
    'price_lakh': [85, 95, 110, 130, 300, 60, 90, 100]  # in Lakhs
}

# Create DataFrame
df = pd.DataFrame(data)

# One-hot encode location
df_encoded = pd.get_dummies(df, columns=['location'], drop_first=True)

# Features and target
X = df_encoded.drop('price_lakh', axis=1)
y = df_encoded['price_lakh']

# Train model
model = LinearRegression()
model.fit(X, y)

# ------------------------
# Streamlit App
# ------------------------
st.title("🏠 Pune House Price Prediction")
st.write("Enter details to predict the house price in Pune")

# User input
location = st.selectbox("Select Location", df['location'].unique())
bhk = st.slider("Number of Bedrooms (BHK)", 1, 5, 2)
sqft = st.number_input("Area (sqft)", min_value=500, max_value=5000, value=1000)

# Prepare input for model
input_data = pd.DataFrame({
    'bhk': [bhk],
    'sqft': [sqft]
})

# Add location encoding
for loc in df_encoded.columns:
    if loc.startswith('location_'):
        input_data[loc] = 1 if loc == f'location_{location}' else 0

# Predict
if st.button("Predict Price"):
    prediction = model.predict(input_data)[0]
    st.success(f"Estimated Price: ₹ {prediction:.2f} Lakhs")
