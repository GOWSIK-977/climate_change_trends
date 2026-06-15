import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from utils.api_client import APIClient

# Page configuration
st.set_page_config(
    page_title="Climate Change Trends Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .warning-text {
        color: #ff6b6b;
        font-weight: bold;
    }
    .success-text {
        color: #51cf66;
        font-weight: bold;
    }
    .info-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🌍 Climate Change Trends Dashboard</h1><p>Real-time analysis of global climate indicators and temperature trends</p></div>', unsafe_allow_html=True)

# Load data
with st.spinner("Loading climate data..."):
    climate_data = APIClient.get_climate_data()
    summary_stats = APIClient.get_summary_stats()
    correlations = APIClient.get_correlations()

if climate_data:
    df = pd.DataFrame(climate_data)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Temperature Increase</h3>
            <h2 style="color: #ff6b6b;">+{summary_stats.get('total_temp_increase', 0)}°C</h2>
            <p>since 1880</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🌡️ Current Temp</h3>
            <h2 style="color: #ff6b6b;">{summary_stats.get('current_temp', 0)}°C</h2>
            <p>Global average</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Decade Change</h3>
            <h2 style="color: #ff6b6b;">+{summary_stats.get('recent_decade_change', 0)}°C</h2>
            <p>Last decade</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        trend_analysis = APIClient.get_trend_analysis('temperature_2m')
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 R² Score</h3>
            <h2 style="color: #51cf66;">{trend_analysis.get('r_squared', 0)}</h2>
            <p>Trend confidence</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Temperature trend chart
    st.markdown("---")
    st.subheader("📊 Temperature Trend Analysis (1880-2023)")
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    if 'temperature_2m' in df.columns and 'relative_humidity_2m' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['Year'], y=df['temperature_2m'], name="Temperature (2m)", line=dict(color='red', width=2)),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=df['Year'], y=df['relative_humidity_2m'], name="Relative Humidity (2m)", line=dict(color='blue', width=2)),
            secondary_y=True
        )
        
        fig.update_layout(
            title="Temperature and Relative Humidity Over Time",
            xaxis_title="Year",
            hovermode='x unified',
            height=500
        )
        
        fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
        fig.update_yaxes(title_text="Relative Humidity (%)", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Required columns not found in data")
    
    # Additional metrics
    st.markdown("---")
    st.subheader("📈 Additional Climate Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'precipitation' in df.columns:
            st.markdown("### Precipitation Trends")
            fig_precip = px.line(df, x='Year', y='precipitation', title="Precipitation Over Time")
            fig_precip.update_layout(height=400)
            st.plotly_chart(fig_precip, use_container_width=True)
    
    with col2:
        if 'wind_speed_10m' in df.columns:
            st.markdown("### Wind Speed Trends")
            fig_wind = px.line(df, x='Year', y='wind_speed_10m', title="Wind Speed Over Time", line_shape='linear')
            fig_wind.update_layout(height=400)
            st.plotly_chart(fig_wind, use_container_width=True)
    
    # Data information
    st.markdown("---")
    st.markdown("### 📊 Dataset Information")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Year Range", f"{int(df['Year'].min())} - {int(df['Year'].max())}")
    with col3:
        st.metric("Data Columns", len(df.columns))
    
    # Display raw data
    with st.expander("View Raw Data"):
        st.dataframe(df.head(20), use_container_width=True)
        st.markdown(f"**Showing 20 of {len(df)} records**")
    
else:
    st.error("Unable to load climate data. Please ensure the backend is running on http://localhost:8000")
    st.info("To start the backend, run: `python -m uvicorn backend.app.main:app --reload`")
