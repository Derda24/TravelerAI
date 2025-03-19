import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# 📌 Sample dataset
data = pd.DataFrame({
    'Travel_Type': ['Adventure', 'Luxury', 'Business', 'Family', 'Cultural', 'Beach', 'Adventure', 'Luxury'],
    'Budget': ['High', 'High', 'Medium', 'Low', 'Medium', 'High', 'Medium', 'High'],
    'Preferred_Region': ['South America', 'Europe', 'Asia', 'Turkey', 'Middle East', 'Southeast Asia', 'North America', 'Caribbean'],
    'Previous_Trips': ['USA, Canada', 'France, Italy', 'Japan', 'Istanbul', 'Egypt', 'Thailand', 'Mexico', 'None'],
    'Recommended_Destination': ['Patagonia, Argentina', 'Santorini, Greece', 'Singapore', 'Cappadocia, Turkey', 
                                 'Petra, Jordan', 'Bali, Indonesia', 'Banff, Canada', 'St. Barts, Caribbean'],
    'Reason': [
        "Ideal for trekking lovers, stunning mountain landscapes and glaciers.",
        "Exclusive resorts with breathtaking sunset views and luxury villas.",
        "A global financial hub with high-end hotels and top-tier business facilities.",
        "A unique mix of history, nature, and hot air balloon rides over fairy chimneys.",
        "Ancient rock-cut architecture and UNESCO World Heritage Site.",
        "Crystal-clear beaches, luxurious resorts, and world-class diving spots.",
        "Hiking, canoeing, and breathtaking turquoise lakes in the Canadian Rockies.",
        "Exclusive beaches, high-end shopping, and Michelin-starred restaurants."
    ]
})

# 📌 Encode categorical data
data_encoded = pd.get_dummies(data, columns=['Travel_Type', 'Budget', 'Preferred_Region'])
X = data_encoded.drop(columns=['Recommended_Destination', 'Reason', 'Previous_Trips'])
y = data[['Recommended_Destination', 'Reason']]

# 📌 Train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y['Recommended_Destination'])

# 📌 Streamlit UI
st.title("AI-Powered Travel Recommendation")
st.write("Tell us about your travel preferences, and we'll recommend a destination!")

# 📌 User input fields
travel_type = st.selectbox("Select Travel Type", data["Travel_Type"].unique())
budget = st.selectbox("Select Budget Level", data["Budget"].unique())
preferred_region = st.selectbox("Preferred Region", data["Preferred_Region"].unique())

# 📌 Predict button
if st.button("Get Recommendation"):
    # Create user input DataFrame
    new_user = pd.DataFrame({
        'Travel_Type': [travel_type],
        'Budget': [budget],
        'Preferred_Region': [preferred_region]
    })

    # Encode new user input
    new_user_encoded = pd.get_dummies(new_user, columns=['Travel_Type', 'Budget', 'Preferred_Region'])

    # Ensure all features match
    for col in X.columns:
        if col not in new_user_encoded:
            new_user_encoded[col] = 0
    new_user_encoded = new_user_encoded[X.columns]

    # Make prediction
    predicted_destination = model.predict(new_user_encoded)
    reason = data[data['Recommended_Destination'] == predicted_destination[0]]['Reason'].values[0]

    # Show result
    st.success(f"📍 Recommended Destination: **{predicted_destination[0]}**")
    st.write(f"💡 Why? {reason}")
