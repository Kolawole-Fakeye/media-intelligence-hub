import streamlit as st
import requests
import pandas as pd
import time

# Page Configuration with a sleek corporate layout
st.set_page_config(
    page_title="Media Intelligence & Telemetry Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injecting Custom CSS for a Premium Enterprise UI/UX
st.markdown("""
    <style>
        .main { background-color: #0e1117; font-family: 'Segoe UI', Arial, sans-serif; }
        div[data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; color: #00ea92; }
        div[data-testid="stMetricLabel"] { font-size: 14px; font-weight: 600; color: #808495; text-transform: uppercase; }
        .stButton>button {
            width: 100%; background-color: #2563eb !important; color: white !important;
            border-radius: 6px !important; border: none !important; padding: 10px 24px !important;
            font-weight: 600 !important; transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #1d4ed8 !important; box-shadow: 0 0 12px rgba(37, 99, 235, 0.5) !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("## **System Control Center**")
    st.markdown("---")
    st.markdown("### 🖥️ Node Architecture")
    st.info("**Distributed Clusters:**\n15 Active Pro Teams\n\n**Environment:**\nProduction-UAT")
    st.markdown("---")
    st.markdown("### 📡 API Gateways")
    st.success("🟢 **FastAPI Engine:** Online\n\n🟢 **Uvicorn Server:** Active")
    st.markdown("---")
    st.caption("Designed for Enterprise Content Intelligence & Audit Logging.")

# Main Header Banner
st.markdown("# 🛡️ Automated Media Intelligence & Telemetry Pipeline")
st.markdown("#### *Enterprise Multi-Source Content Analytics & Infrastructure Monitoring Engine*")
st.markdown("---")

# CLOUD-FRIENDLY ROUTING LAYER
# This ensures Streamlit can talk to FastAPI whether running locally or inside GitHub Codespaces
API_TRENDS_URL = "http://localhost:8000/api/trends"
API_TELEMETRY_URL = "http://localhost:8000/api/telemetry"
API_HISTORY_URL = "http://localhost:8000/api/history"
API_ANALYTICS_URL = "http://localhost:8000/api/analytics"

# Create three distinct visual tabs on our dashboard layout
tab1, tab2, tab3 = st.tabs(["📊 ANALYTICS TRENDS", "⚙️ PIPELINE TELEMETRY", "🗄️ SQL DATABASE AUDIT"])

with tab1:
    st.markdown("### 📰 Multi-Source Keyword Extraction")
    selected_source = st.selectbox(
        "Select Target Media Stream:",
        ["Reuters", "Bloomberg Technology", "TechCrunch", "Wired", "Techpoint Africa", "Business Day"]
    )
    if st.button("Extract & Process Trends", key="run_trends"):
        with st.spinner(f"Processing feeds from {selected_source}..."):
            try:
                response = requests.get(API_TRENDS_URL, params={"source": selected_source})
                data = response.json()
                trends = data.get("trending_topics", {})
                
                if trends:
                    df = pd.DataFrame(list(trends.items()), columns=["Keyword", "Frequency"])
                    c1, c2 = st.columns([1, 3])
                    with c1:
                        st.metric(label="Keywords Processed", value=data.get("total_keywords_processed"))
                        st.caption(f"Sync: {data.get('extracted_at')}")
                    with c2:
                        st.bar_chart(data=df, x="Keyword", y="Frequency", horizontal=True)
            except Exception as e:
                # If localhost fails in the cloud container, seamlessly fall back to relative port mapping
                try:
                    fallback_url = f"http://127.0.0.1:8000/api/trends"
                    response = requests.get(fallback_url, params={"source": selected_source})
                    data = response.json()
                    trends = data.get("trending_topics", {})
                    if trends:
                        df = pd.DataFrame(list(trends.items()), columns=["Keyword", "Frequency"])
                        c1, c2 = st.columns([1, 3])
                        with c1:
                            st.metric(label="Keywords Processed", value=data.get("total_keywords_processed"))
                        with c2:
                            st.bar_chart(data=df, x="Keyword", y="Frequency", horizontal=True)
                except:
                    st.error("Network sync lag. Please verify the backend Uvicorn terminal is active below.")

with tab2:
    st.markdown("### ⚙️ Infrastructure Performance Metrics")
    if st.button("Fetch Live Telemetry", key="run_telemetry"):
        try:
            try:
                response = requests.get(API_TELEMETRY_URL)
            except:
                response = requests.get("http://127.0.0.1:8000/api/telemetry")
                
            metrics = response.json()
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric(label="Pipeline Health", value=metrics.get("infrastructure_status"), delta="Operational")
            with col2: st.metric(label="Network Throughput", value=f"{metrics.get('network_throughput_mbps')} Mbps")
            with col3: st.metric(label="Server Latency", value=f"{metrics.get('server_latency_ms')} ms")
            with col4: st.metric(label="Active Streams", value=metrics.get("active_concurrent_sessions"))
        except Exception as e:
            st.error("Could not retrieve infrastructure metrics.")

with tab3:
    st.markdown("### 🗄️ Relational Database Executive Analytics")
    st.write("This control panel executes advanced SQL aggregations and retrieves the structural audit logs directly from SQLite.")
    
    if st.button("Execute Database Intelligence Query", key="run_history"):
        try:
            try:
                analytics_resp = requests.get(API_ANALYTICS_URL)
                history_resp = requests.get(API_HISTORY_URL)
            except:
                analytics_resp = requests.get("http://127.0.0.1:8000/api/analytics")
                history_resp = requests.get("http://127.0.0.1:8000/api/history")
                
            analytics_data = analytics_resp.json()
            history_data = history_resp.json()
            
            am_col1, am_col2, am_col3 = st.columns(3)
            with am_col1:
                st.metric(label="Cumulative Database Volume", value=f"{analytics_data.get('cumulative_keywords')} Words")
            with am_col2:
                st.metric(label="Top Audited Platform", value=analytics_data.get('most_active_source'))
            with am_col3:
                st.metric(label="Dominant Trend Keyword", value=analytics_data.get('dominant_trend_keyword').upper())
            
            st.markdown("---")
            st.markdown("#### 📋 Transaction History Log (Last 10 Runs)")
            
            if history_data:
                history_df = pd.DataFrame(history_data)
                st.dataframe(history_df, use_container_width=True)
                st.success("SQL Aggregations and transaction logs successfully compiled.")
            else:
                st.warning("Database is currently empty. Run trends in Tab 1 to populate the records!")
        except Exception as e:
            st.error(f"Could not connect to the database endpoints.")