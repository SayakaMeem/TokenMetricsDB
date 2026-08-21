import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="TokenMetrics Analytics Engine",
    page_icon="⚡",
    layout="wide"
)

API_URL = "https://tokenmetricsdb.onrender.com/api/v1/metrics/summary"

# Custom Styling
st.markdown("""
    <style>
        .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
        div[data-testid="stMetricValue"] {font-size: 2rem; font-weight: 700;}
    </style>
""", unsafe_allow_html=True)

# Header Section
st.title("⚡ TokenMetrics Analytics Engine")
st.caption("Real-time monitoring of LLM usage costs, token throughput, and model latency distribution.")

# Fetch Data with Cache
@st.cache_data(ttl=5)
def fetch_data():
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None

data = fetch_data()

# Error State / Cold-Start Handling
if not data:
    st.error("Failed to connect to live backend API. Click Refresh below to wake up the Render instance.")
    if st.button("🔄 Retry Connection"):
        st.cache_data.clear()
        st.rerun()
else:
    # Safe Parsing Logic (Handles both new nested format and legacy flat format)
    if "summary" in data:
        summary = data["summary"]
        hourly = pd.DataFrame(data.get("hourly_trends", []))
        models = pd.DataFrame(data.get("model_breakdown", []))
    else:
        summary = data
        hourly = pd.DataFrame([])
        models = pd.DataFrame([])

    # Top Control Bar
    col_title, col_btn = st.columns([4, 1])
    with col_btn:
        if st.button("🔄 Live Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    st.markdown("---")

    # KPI Summary Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    # Safely get values with defaults if keys are missing in legacy payloads
    total_tokens = summary.get('total_tokens', 0)
    total_cost = summary.get('total_cost', 0.0)
    avg_latency = summary.get('avg_latency_ms', 0)
    active_models = summary.get('active_models', 0)

    kpi1.metric("Total Tokens", f"{total_tokens:,}", delta="+4.2%")
    kpi2.metric("Total Cost ($)", f"${total_cost:.2f}", delta="+$0.85")
    kpi3.metric("Avg Latency", f"{avg_latency} ms", delta="-12 ms", delta_color="inverse")
    kpi4.metric("Active Models", active_models, delta="Operational")

    st.markdown("---")

    # Dynamic Visualizations (Rendered when time-series data is available)
    if not hourly.empty and not models.empty:
        chart_col1, chart_col2 = st.columns([2, 1])

        with chart_col1:
            st.subheader("📈 24-Hour Token Throughput & Cost Trend")
            fig_trend = px.area(
                hourly, 
                x="time", 
                y="tokens", 
                hover_data=["cost", "latency"],
                color_discrete_sequence=["#00CC96"],
                labels={"time": "Time (UTC)", "tokens": "Tokens Processed"}
            )
            fig_trend.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=320
            )
            st.plotly_chart(fig_trend, use_container_width=True)

        with chart_col2:
            st.subheader("🧩 Cost Distribution by Model")
            fig_donut = px.pie(
                models, 
                names="model", 
                values="cost", 
                hole=0.55,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_donut.update_layout(
                margin=dict(l=10, r=10, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                height=320,
                showlegend=True
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        # Detailed Latency Bar Chart
        st.subheader("⏱️ Hourly Latency Variations (ms)")
        fig_bar = px.bar(
            hourly, 
            x="time", 
            y="latency", 
            color="latency", 
            color_continuous_scale="Viridis",
            labels={"time": "Time", "latency": "Latency (ms)"}
        )
        fig_bar.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=250
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Backend deployment is updating. Detailed time-series charts will display automatically once the updated API endpoint is live.")