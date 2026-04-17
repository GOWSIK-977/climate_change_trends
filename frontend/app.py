import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942803.png", width=80)
    st.title("🌍 Navigation")
    page = st.radio(
        "Go to",
        ["🏠 Dashboard", "📈 Trend Analysis", "⚠️ Anomaly Detection", "📊 Reports & Insights"]
    )
    
    st.markdown("---")
    st.info(
        """
        **Data Source:** Global Climate Dataset (1880-2023)
        
        **Metrics Tracked:**
        - Global Temperature
        - CO2 Levels
        - Sea Level Rise
        """
    )

# Main content
if page == "🏠 Dashboard":
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
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎯 R² Score</h3>
                <h2 style="color: #51cf66;">{APIClient.get_trend_analysis('Global_Temp').get('r_squared', 0)}</h2>
                <p>Trend confidence</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Temperature trend chart
        st.markdown("---")
        st.subheader("📊 Temperature Trend Analysis (1880-2023)")
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=df['Year'], y=df['Global_Temp'], name="Global Temperature", line=dict(color='red', width=2)),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=df['Year'], y=df['CO2_Levels'], name="CO2 Levels", line=dict(color='blue', width=2)),
            secondary_y=True
        )
        
        fig.update_layout(
            title="Temperature and CO2 Levels Over Time",
            xaxis_title="Year",
            hovermode='x unified',
            height=500
        )
        
        fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
        fig.update_yaxes(title_text="CO2 (ppm)", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlations section
        st.subheader("🔗 Key Correlations")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Temperature vs CO2</h4>
                <h2>{correlations.get('temp_co2', 0)}</h2>
                <p>{correlations.get('interpretations', {}).get('temp_co2', '')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Temperature vs Sea Level</h4>
                <h2>{correlations.get('temp_sea', 0)}</h2>
                <p>{correlations.get('interpretations', {}).get('temp_sea', '')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h4>CO2 vs Sea Level</h4>
                <h2>{correlations.get('co2_sea', 0)}</h2>
                <p>{correlations.get('interpretations', {}).get('co2_sea', '')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Data table
        with st.expander("📋 View Raw Climate Data"):
            st.dataframe(df, use_container_width=True)

elif page == "📈 Trend Analysis":
    st.title("📈 Climate Trend Analysis")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        metric = st.selectbox(
            "Select Metric",
            ["Global_Temp", "CO2_Levels", "Sea_Level_Rise"],
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        if st.button("Analyze Trend", type="primary"):
            with st.spinner("Analyzing trends..."):
                trend_data = APIClient.get_trend_analysis(metric)
                
                if trend_data:
                    st.markdown("### 📊 Trend Statistics")
                    
                    st.metric("Trend Direction", trend_data.get('trend', 'N/A'))
                    st.metric("Slope (per year)", f"{trend_data.get('slope', 0)} °C")
                    st.metric("Slope (per decade)", f"{trend_data.get('slope_per_decade', 0)} °C")
                    st.metric("R-squared", f"{trend_data.get('r_squared', 0)}")
                    st.metric("P-value", f"{trend_data.get('p_value', 0)}")
                    st.metric("95% CI", f"[{trend_data.get('ci_lower', 0)}, {trend_data.get('ci_upper', 0)}]")
                    
                    if trend_data.get('p_value', 1) < 0.05:
                        st.success("✅ This trend is statistically significant (p < 0.05)")
                    else:
                        st.warning("⚠️ This trend may not be statistically significant")
    
    with col2:
        climate_data = APIClient.get_climate_data()
        if climate_data:
            df = pd.DataFrame(climate_data)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['Year'], 
                y=df[metric], 
                mode='lines+markers',
                name=metric.replace('_', ' '),
                line=dict(width=2)
            ))
            
            # Add trend line
            from scipy import stats
            slope, intercept, r_value, p_value, std_err = stats.linregress(df['Year'], df[metric])
            trend_line = slope * df['Year'] + intercept
            fig.add_trace(go.Scatter(
                x=df['Year'],
                y=trend_line,
                mode='lines',
                name='Trend Line',
                line=dict(dash='dash', color='red')
            ))
            
            fig.update_layout(
                title=f"{metric.replace('_', ' ').title()} Trend Analysis",
                xaxis_title="Year",
                yaxis_title=metric.replace('_', ' '),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)

elif page == "⚠️ Anomaly Detection":
    st.title("⚠️ Climate Anomaly Detection")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        metric = st.selectbox(
            "Select Metric for Anomaly Detection",
            ["Global_Temp", "CO2_Levels", "Sea_Level_Rise"],
            format_func=lambda x: x.replace('_', ' ').title(),
            key="anomaly_metric"
        )
        
        threshold = st.slider("Anomaly Threshold (Z-score)", 1.5, 3.0, 2.0, 0.1)
        
        if st.button("Detect Anomalies", type="primary"):
            with st.spinner("Detecting anomalies..."):
                anomaly_data = APIClient.get_anomalies(metric, threshold)
                
                if anomaly_data:
                    st.markdown(f"### 📊 Anomaly Results")
                    st.metric("Total Anomalies Detected", anomaly_data.get('total_anomalies', 0))
                    
                    anomalies = anomaly_data.get('anomalies', [])
                    anomaly_years = [a for a in anomalies if a['is_anomaly']]
                    
                    if anomaly_years:
                        st.markdown("#### 🔴 Anomalous Years:")
                        for anomaly in anomaly_years[:10]:
                            severity_icon = "🔴" if anomaly['severity'] == "High" else "🟡"
                            st.write(f"{severity_icon} **{anomaly['year']}**: {anomaly['value']} (Z-score: {anomaly['z_score']})")
    
    with col2:
        climate_data = APIClient.get_climate_data()
        if climate_data:
            df = pd.DataFrame(climate_data)
            
            # Calculate Z-scores
            mean_val = df[metric].mean()
            std_val = df[metric].std()
            df['z_score'] = (df[metric] - mean_val) / std_val
            df['is_anomaly'] = abs(df['z_score']) > threshold
            
            # Create visualization
            fig = go.Figure()
            
            # Normal points
            normal_df = df[~df['is_anomaly']]
            fig.add_trace(go.Scatter(
                x=normal_df['Year'], 
                y=normal_df[metric],
                mode='lines+markers',
                name='Normal',
                line=dict(color='blue', width=2)
            ))
            
            # Anomaly points
            anomaly_df = df[df['is_anomaly']]
            fig.add_trace(go.Scatter(
                x=anomaly_df['Year'],
                y=anomaly_df[metric],
                mode='markers',
                name='Anomaly',
                marker=dict(color='red', size=10, symbol='x')
            ))
            
            fig.update_layout(
                title=f"Anomaly Detection - {metric.replace('_', ' ').title()}",
                xaxis_title="Year",
                yaxis_title=metric.replace('_', ' '),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)

elif page == "📊 Reports & Insights":
    st.title("📊 Climate Insights & Recommendations")
    
    with st.spinner("Generating comprehensive report..."):
        report = APIClient.generate_report()
        forecast = APIClient.get_forecast(10)
        correlations = APIClient.get_correlations()
    
    if report:
        # Critical Findings
        st.markdown("## 🔴 Critical Findings")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"**Temperature Increase**\n\n+{report.get('temp_increase', 0)}°C since 1880")
        
        with col2:
            st.warning(f"**Warming Rate**\n\n{report.get('temperature_trend', {}).get('slope_per_decade', 0)}°C per decade")
        
        with col3:
            st.error(f"**Anomalies**\n\n{report.get('anomaly_count', 0)} significant anomalies detected")
        
        # Forecast
        st.markdown("## 🔮 Temperature Forecast (Next 10 Years)")
        if forecast.get('forecast'):
            forecast_df = pd.DataFrame(forecast['forecast'])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=forecast_df['year'],
                y=forecast_df['predicted_temp'],
                mode='lines+markers',
                name='Forecast',
                line=dict(color='red', width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast_df['year'],
                y=forecast_df['ci_upper'],
                mode='lines',
                name='Upper CI',
                line=dict(dash='dash', color='gray')
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast_df['year'],
                y=forecast_df['ci_lower'],
                mode='lines',
                name='Lower CI',
                line=dict(dash='dash', color='gray'),
                fill='tonexty'
            ))
            
            fig.update_layout(
                title="Global Temperature Forecast with 95% Confidence Intervals",
                xaxis_title="Year",
                yaxis_title="Temperature (°C)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(f"""
            <div class="info-box">
                <p>⚠️ <strong>Projection:</strong> By 2033, global temperature is projected to reach approximately 
                <strong>{forecast_df['predicted_temp'].iloc[-1]}°C</strong>, representing an additional warming of 
                <strong>{round(forecast_df['predicted_temp'].iloc[-1] - forecast_df['predicted_temp'].iloc[0], 2)}°C</strong> 
                from current levels.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Sustainability Recommendations
        st.markdown("## ♻️ Sustainability Recommendations")
        
        recommendations = [
            {
                "title": "1. Accelerate Renewable Energy Transition",
                "description": "Target 80% renewable energy by 2030 to reduce CO2 emissions by 50% from 2020 levels.",
                "urgency": "High",
                "timeline": "2024-2030"
            },
            {
                "title": "2. Implement Carbon Capture Technologies",
                "description": "Deploy large-scale direct air capture facilities in industrial zones.",
                "urgency": "Medium",
                "timeline": "2025-2035"
            },
            {
                "title": "3. Coastal Protection Infrastructure",
                "description": f"With sea level rise accelerating at {report.get('sea_level_trend', {}).get('slope', 0)} mm/year, invest in coastal defenses.",
                "urgency": "High",
                "timeline": "Immediate"
            },
            {
                "title": "4. Climate-Resilient Agriculture",
                "description": "Develop heat-resistant crop varieties and water-efficient irrigation systems.",
                "urgency": "Medium",
                "timeline": "2024-2030"
            },
            {
                "title": "5. Enhanced Monitoring Network",
                "description": "Expand climate monitoring stations in vulnerable regions for early warning systems.",
                "urgency": "Low",
                "timeline": "2024-2028"
            }
        ]
        
        for rec in recommendations:
            with st.expander(f"{rec['title']} - Urgency: {rec['urgency']} | Timeline: {rec['timeline']}"):
                st.write(rec['description'])
        
        # Action Plan
        st.markdown("## 📋 Action Plan")
        
        action_items = {
            "Immediate (2024)": [
                "Reduce carbon emissions by 7.6% annually",
                "Implement carbon pricing mechanisms",
                "Launch public awareness campaigns"
            ],
            "Short-term (2025-2027)": [
                "Achieve 40% renewable energy adoption",
                "Phase out coal power plants",
                "Implement building efficiency standards"
            ],
            "Medium-term (2028-2035)": [
                "Achieve net-zero electricity generation",
                "Electrify public transportation",
                "Restore 30% of degraded forests"
            ],
            "Long-term (2036-2050)": [
                "Complete transition to circular economy",
                "Achieve carbon negativity",
                "Protect 50% of oceans and lands"
            ]
        }
        
        for period, items in action_items.items():
            st.markdown(f"### {period}")
            for item in items:
                st.checkbox(item, key=f"{period}_{item}")
        
        # Download Report Button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📥 Download Full Report", use_container_width=True):
                report_text = f"""
                CLIMATE CHANGE TRENDS REPORT
                =============================
                
                Key Findings:
                - Temperature Increase: {report.get('temp_increase', 0)}°C since 1880
                - Current Warming Rate: {report.get('temperature_trend', {}).get('slope_per_decade', 0)}°C/decade
                - CO2-Temperature Correlation: {correlations.get('temp_co2', 0)}
                - Anomalies Detected: {report.get('anomaly_count', 0)}
                
                Statistical Significance:
                - R-squared: {report.get('temperature_trend', {}).get('r_squared', 0)}
                - P-value: {report.get('temperature_trend', {}).get('p_value', 0)}
                
                Forecast (2033):
                - Projected Temperature: {forecast.get('forecast', [{}])[-1].get('predicted_temp', 'N/A')}°C
                
                Generated by Climate Change Trends Analysis System
                Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                st.download_button(
                    label="💾 Download as Text",
                    data=report_text,
                    file_name="climate_report.txt",
                    mime="text/plain"
                )