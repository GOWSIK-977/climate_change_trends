import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from utils.api_client import APIClient

st.set_page_config(
    page_title="Anomaly Detection",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ Anomaly Detection")

st.markdown("""
Detect unusual climate events and extreme deviations from normal patterns using 
statistical analysis (Z-score method). Anomalies are identified based on how many 
standard deviations they deviate from the mean.
""")

# Sidebar settings
with st.sidebar:
    st.subheader("Detection Settings")
    
    selected_metric = st.selectbox(
        "Select metric for anomaly detection:",
        ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
        index=0
    )
    
    threshold = st.slider(
        "Z-score threshold:",
        min_value=1.0,
        max_value=5.0,
        value=2.0,
        step=0.5,
        help="Higher threshold = fewer anomalies detected"
    )
    
    st.markdown("""
    ### Understanding Z-scores:
    - **Z-score**: Number of standard deviations from the mean
    - **> 2**: Unusual (Moderate severity)
    - **> 3**: Very unusual (High severity)
    - **> 4**: Extremely rare (Critical severity)
    """)

# Load data
with st.spinner(f"Detecting anomalies in {selected_metric}..."):
    climate_data = APIClient.get_climate_data()
    anomalies_response = APIClient.get_anomalies(selected_metric, threshold)

if climate_data and anomalies_response:
    df = pd.DataFrame(climate_data)
    anomalies_data = anomalies_response.get('anomalies', [])
    total_anomalies = anomalies_response.get('total_anomalies', 0)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    high_severity = len([a for a in anomalies_data if a.get('severity') == 'High'])
    moderate_severity = len([a for a in anomalies_data if a.get('severity') == 'Moderate'])
    low_severity = len([a for a in anomalies_data if a.get('severity') == 'Low'])
    
    with col1:
        st.metric("🔴 High Severity", high_severity)
    
    with col2:
        st.metric("🟡 Moderate Severity", moderate_severity)
    
    with col3:
        st.metric("🟢 Low Severity", low_severity)
    
    with col4:
        st.metric("📊 Total Anomalies", total_anomalies)
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["Data Table", "Visualization", "Analysis"])
    
    with tab1:
        st.subheader("Anomaly Details")
        
        if anomalies_data:
            # Create DataFrame for display
            anomaly_df = pd.DataFrame(anomalies_data)
            
            # Color code severity
            def severity_color(severity):
                if severity == 'High':
                    return '🔴'
                elif severity == 'Moderate':
                    return '🟡'
                else:
                    return '🟢'
            
            # Display table
            st.dataframe(
                anomaly_df.style.apply(
                    lambda x: ['background-color: #ffcccc' if x['severity'] == 'High' 
                               else 'background-color: #ffffcc' if x['severity'] == 'Moderate'
                               else 'background-color: #ccffcc' for _ in x],
                    axis=1,
                    subset=['severity']
                ),
                use_container_width=True
            )
            
            # Download option
            csv = anomaly_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Anomalies as CSV",
                data=csv,
                file_name=f"anomalies_{selected_metric}.csv",
                mime="text/csv"
            )
        else:
            st.info(f"No anomalies detected with threshold {threshold} for {selected_metric}")
    
    with tab2:
        st.subheader("Anomaly Visualization")
        
        if selected_metric in df.columns and anomalies_data:
            # Calculate mean and std for visualization
            mean_val = df[selected_metric].mean()
            std_val = df[selected_metric].std()
            
            fig = go.Figure()
            
            # Add main data line
            fig.add_trace(go.Scatter(
                x=df['Year'],
                y=df[selected_metric],
                mode='lines',
                name='Data',
                line=dict(color='blue', width=2)
            ))
            
            # Add mean line
            fig.add_hline(y=mean_val, line_dash="dash", line_color="green", 
                         annotation_text="Mean", annotation_position="right")
            
            # Add threshold bands
            fig.add_hline(y=mean_val + threshold * std_val, line_dash="dot", line_color="orange",
                         annotation_text=f"threshold (+{threshold}σ)", annotation_position="right")
            fig.add_hline(y=mean_val - threshold * std_val, line_dash="dot", line_color="orange",
                         annotation_text=f"threshold (-{threshold}σ)", annotation_position="right")
            
            # Highlight anomalies
            anomaly_years = [a['year'] for a in anomalies_data if a['is_anomaly']]
            anomaly_values = [df[df['Year'] == year][selected_metric].iloc[0] 
                            for year in anomaly_years if year in df['Year'].values]
            
            if anomaly_years and anomaly_values:
                fig.add_trace(go.Scatter(
                    x=anomaly_years,
                    y=anomaly_values,
                    mode='markers',
                    name='Anomalies',
                    marker=dict(size=12, color='red', symbol='star', line=dict(width=2, color='darkred'))
                ))
            
            fig.update_layout(
                title=f"Anomaly Detection in {selected_metric}",
                xaxis_title="Year",
                yaxis_title="Value",
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Unable to visualize anomalies")
    
    with tab3:
        st.subheader("Analysis & Interpretation")
        
        if selected_metric in df.columns:
            mean_val = df[selected_metric].mean()
            std_val = df[selected_metric].std()
            
            analysis_text = f"""
            ### Dataset Statistics
            - **Mean**: {mean_val:.3f}
            - **Std Dev**: {std_val:.3f}
            - **Min**: {df[selected_metric].min():.3f}
            - **Max**: {df[selected_metric].max():.3f}
            
            ### Anomaly Detection Method
            The Z-score method identifies anomalies by comparing each value to the population mean:
            
            **Z-score = (Value - Mean) / Standard Deviation**
            
            - **Z-score > {threshold}**: Moderately unusual (appears ~5% of the time in normal distribution)
            - **Z-score > 3**: Highly unusual (appears ~0.3% of the time)
            - **Z-score > 4**: Extremely rare (appears ~0.006% of the time)
            
            ### Thresholds Set
            - **Upper threshold**: {mean_val + threshold * std_val:.3f}
            - **Lower threshold**: {mean_val - threshold * std_val:.3f}
            
            ### Anomalies Found
            - **High Severity (|Z| > 3)**: {high_severity} events
            - **Moderate Severity (|Z| {threshold}-3)**: {moderate_severity} events
            - **Total Anomalies**: {total_anomalies} events
            
            ### Climate Implications
            Anomalies in climate data can indicate:
            - Extreme weather events
            - Unusual seasonal patterns
            - Potential data collection errors
            - Significant climate shifts
            
            High-severity anomalies deserve particular attention for further investigation.
            """
            
            st.markdown(analysis_text)

else:
    st.error("Unable to load anomaly detection data.")
    st.info("Please ensure the backend is running on http://localhost:8000")
