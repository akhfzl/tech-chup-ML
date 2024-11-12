import streamlit as st
import requests
from datetime import datetime

st.title("Wait Time Prediction App")
st.write("Enter the patient’s information to predict the expected wait time.")

arrival_time = st.text_input("Arrival Time (format: %d-%m-%Y %H:%M)", "30-03-2023 12:00")
start_time = st.text_input("Start Time (format: %d-%m-%Y %H:%M)", "30-03-2023 12:15")
queue_length = st.number_input("Queue Length", min_value=0, max_value=100, value=10)

if st.button("Predict Wait Time"):
    try:
        arrival_time_dt = datetime.strptime(arrival_time, "%d-%m-%Y %H:%M")
        start_time_dt = datetime.strptime(start_time, "%d-%m-%Y %H:%M")

        payload = {
            "arrival_time": arrival_time,
            "start_time": start_time,
            "queue_length": queue_length
        }

        response = requests.post("http://localhost:8000/predict_wait_time", json=payload)
        response_data = response.json()

        if response.status_code == 200:
            wait_time = response_data['predicted_wait_time']
            st.success(f"Predicted Wait Time: {wait_time} minutes")
        else:
            st.error("Failed to get prediction from the API.")
    except Exception as e:
        st.error(f"Error: {e}")
