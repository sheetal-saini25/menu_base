import os
import pandas as pd
import streamlit as st
import joblib
from twilio.rest import Client  # ✅ Import the Twilio client

# Title
st.title("📊 AI Utility Dashboard")

# --- 1. Load CSV ---

try:
    dataset = pd.read_csv("ml1.csv")
    st.success("Loaded ml1.csv successfully.")
except FileNotFoundError:
    st.warning("ml1.csv not found. Please upload it below.")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        dataset = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        st.dataframe(dataset)

# --- 2. Salary Prediction ---
st.subheader("💼 Predict Employee Salary")

try:
    model = joblib.load('my_Salary_model.pkl')
    Exp = st.number_input("Enter your Experience (years):", min_value=1, max_value=30)
    if st.button("Predict Salary"):
        result = model.predict([[Exp]])
        st.success(f"Predicted Salary: ₹ {result[0]:,.2f}")
except FileNotFoundError:
    st.error("Model file 'my_Salary_model.pkl' not found. Please check your path.")

# --- 3. Send SMS ---
st.subheader("📩 Send SMS via Twilio")

with st.form("sms_form"):
    twilio_sid = st.text_input("Twilio SID", type="password")
    twilio_token = st.text_input("Twilio Auth Token", type="password")
    twilio_number = st.text_input("Twilio Phone Number (with +country code)")
    recipient_number = st.text_input("Recipient Phone Number (with +country code)")
    sms_body = st.text_input("Message Text", value="Hello from Python!")
    sms_submit = st.form_submit_button("Send SMS")

    if sms_submit:
        try:
            client = Client(twilio_sid, twilio_token)
            message = client.messages.create(
                body=sms_body,
                from_=twilio_number,
                to=recipient_number
            )
            st.success(f"✅ SMS sent successfully! SID: {message.sid}")
        except Exception as e:
            st.error(f"❌ SMS sending failed: {e}")

# --- 4. Make a Call ---
st.subheader("📞 Make a Voice Call via Twilio")

with st.form("call_form"):
    call_sid = st.text_input("Twilio SID (Call)", type="password")
    call_token = st.text_input("Twilio Auth Token (Call)", type="password")
    call_from = st.text_input("Twilio Phone Number (Call)")
    call_to = st.text_input("Recipient Phone Number (Call)")
    call_msg = st.text_area("Call Message", value="Hello! This is a Python-Twilio call. Have a great day!")
    call_submit = st.form_submit_button("Make Call")

    if call_submit:
        try:
            call_client = Client(call_sid, call_token)
            twiml = f'<Response><Say>{call_msg}</Say></Response>'
            call = call_client.calls.create(
                to=call_to,
                from_=call_from,
                twiml=twiml
            )
            st.success(f"✅ Call initiated! SID: {call.sid}")
        except Exception as e:
            st.error(f"❌ Call initiation failed: {e}")
