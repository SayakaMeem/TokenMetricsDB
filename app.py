import streamlit as st
import requests

st.set_page_config(page_title="TokenMetrics Analytics Engine", layout="wide")

st.title("⚡ TokenMetrics Analytics Engine")
st.caption("Real-time monitoring of LLM usage costs and system latency.")

# Define backend API URL
API_URL = "https://tokenmetrics-api.onrender.com/api/v1/metrics/summary"

try:
    response = requests.get(API_URL, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        
        # Display key metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Tokens", f"{data.get('total_tokens', 0):,}")
        col2.metric("Total Cost ($)", f"${data.get('total_cost', 0.0):.2f}")
        col3.metric("Avg Latency", f"{data.get('avg_latency_ms', 0)} ms")
        col4.metric("Active Models", data.get("active_models", 0))
    else:
        st.error(f"Backend returned status code: {response.status_code}")
        st.code(response.text)

except requests.exceptions.ConnectionError:
    st.error("Could not connect to FastAPI backend. Ensure uvicorn is running on port 8000.")