import os
import uuid
import requests
import streamlit as st
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Ensure a persistent user_id across form submissions
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

st.set_page_config(page_title="Ops Coordination", page_icon="🏗️")

FASTAPI_BASE = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000")
OPS_URL = f"{FASTAPI_BASE}/solar/form"

st.title("🚀 GetSolar Ops Coordination Test Form")
st.markdown(
    """
Use this form to simulate an incoming lead for **qualification**, **booking**, **cancellation**, or **rejection**.  
Fill in the fields below and hit **Submit** to POST into your FastAPI Ops endpoint.
"""
)

with st.form("lead_form", clear_on_submit=True):
    # Display the persistent lead_id
    user_id = st.text_input("User ID", value=st.session_state.user_id, disabled=True)

    name            = st.text_input("Name", help="Customer’s full name")
    email           = st.text_input("Email", help="Customer’s email address")
    phone           = st.text_input("Phone Number", help="Customer’s contact number")
    address         = st.text_input("Address", help="Property or billing address")
    company         = st.text_input("Company", help="Company name, if applicable")
    referral_source = st.selectbox(
        "Referral Source",
        options=["Website", "Email", "Social Media", "Friend/Referral", "Other"],
        help="How did the lead hear about GetSolar?"
    )
    budget          = st.number_input(
        "Estimated Budget (SGD)",
        min_value=0,
        step=100,
        help="Approximate budget for the solar system"
    )
    timeline_months = st.number_input(
        "Timeline (Months)",
        min_value=0,
        max_value=60,
        step=1,
        help="Expected installation timeframe in months"
    )
    interest_level  = st.select_slider(
        "Interest Level",
        options=["Low", "Medium", "High"],
        help="How interested is the lead?"
    )
    requested_capacity = st.text_input(
        "Requested Capacity (kW)",
        help="Desired system capacity"
    )

    enquiry = st.text_area("Enquiry", help="Customer's enquiry or message")

    submitted = st.form_submit_button("Submit")


def get_form_response(server_url: str, body: dict):
    """
    Sends the form data to the FastAPI backend and returns the response.
    """
    try:
        response = requests.post(server_url, json=body, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Request to {server_url} failed: {e}")
        return {"error": str(e)}


if submitted:
    body = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "company": company,
        "referral_source": referral_source,
        "budget": budget,
        "timeline_months": timeline_months,
        "interest_level": interest_level,
        "requested_capacity": requested_capacity,
        "enquiry": enquiry,
    }

    st.write("### 🚚 Sending information")
    st.json(body)

    result = get_form_response(OPS_URL, body)
    if result.get("error"):
        st.error(f"❌ Request failed: {result['error']}")
    else:
        st.success("✅ Form submitted successfully!")
        st.balloons()
        st.json(result)