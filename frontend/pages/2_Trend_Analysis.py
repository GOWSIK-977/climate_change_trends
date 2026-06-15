import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from utils.api_client import APIClient

st.set_page_config(
    page_title="Trend Analysis",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Trend Analysis")

st.markdown("""
Analyze climate trends over time using statistical methods including linear regression,
confidence intervals, and trend significance testing.
""")

# Select metric
with st.sidebar:
    st.subheader("Analysis Settings")
    
    selected_metric = st.selectbox(
        "Select metric to analyze:",
        ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
        index=0
    )

# Load data
with st.spinner(f"Analyzing {selected_metric} trends..."):
    climate_data = APIClient.get_climate_data()
    trend_analysis = APIClient.get_trend_analysis(selected_metric)

if climate_data and trend_analysis:
    df = pd.DataFrame(climate_data)
    
    # Display trend metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Trend Direction",
            trend_analysis.get('trend', 'Unknown'),
            f"Slope: {trend_analysis.get('slope', 0)}"
        )
    
    with col2:
        st.metric(
            "Change per Decade",
            f"{trend_analysis.get('slope_per_decade', 0)} units",
            f"R²: {trend_analysis.get('r_squared', 0)}"
        )
    
    with col3:
        p_value = trend_analysis.get('p_value', 1)
        significance = "✓ Significant" if p_value < 0.05 else "Not Significant"
        st.metric(
            "Statistical Significance",
            significance,
            f"p-value: {p_value}"
        )
    
    with col4:
        st.metric(
            "Model Fit (R²)",
            f"{float(trend_analysis.get('r_squared', 0)) * 100:.1f}%",
            "Variance explained"
        )
    
    st.markdown("---")
    
    # Visualization
    st.subheader("Trend Visualization")
    
    tab1, tab2, tab3 = st.tabs(["Chart", "Statistics", "Details"])
    
    with tab1:
        # Line chart with trend
        if selected_metric in df.columns:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['Year'],
                y=df[selected_metric],
                mode='lines',
                name='Observed Data',
                line=dict(color='blue', width=2)
            ))
            
            # Add trend line
            if len(df) > 1:
                X = df['Year'].values
                y = df[selected_metric].values
                z = np.polyfit(X, y, 1)
                p = np.poly1d(z)
                trend_line = p(X)
                
                fig.add_trace(go.Scatter(
                    x=df['Year'],
                    y=trend_line,
                    mode='lines',
                    name='Trend Line',
                    line=dict(color='red', width=2, dash='dash')
                ))
            
            fig.update_layout(
                title=f"{selected_metric} Trend Analysis",
                xaxis_title="Year",
                yaxis_title="Value",
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Statistical Details")
        
        stats_text = f"""
        **Metric**: {selected_metric}
        
        **Trend Direction**: {trend_analysis.get('trend', 'Unknown')}
        
        **Slope (per year)**: {trend_analysis.get('slope', 'N/A')} units/year
        
        **Slope per decade**: {trend_analysis.get('slope_per_decade', 'N/A')} units/decade
        
        **Intercept**: {trend_analysis.get('intercept', 'N/A')}
        
        **R-squared (R²)**: {trend_analysis.get('r_squared', 'N/A')} 
        - *Explains {float(trend_analysis.get('r_squared', 0)) * 100:.1f}% of the variation*
        
        **P-value**: {trend_analysis.get('p_value', 'N/A')}
        - *Significance: {'✓ Statistically significant (p < 0.05)' if float(trend_analysis.get('p_value', 1)) < 0.05 else 'Not statistically significant (p ≥ 0.05)'}*
        
        **95% Confidence Interval**:
        - Lower bound: {trend_analysis.get('ci_lower', 'N/A')}
        - Upper bound: {trend_analysis.get('ci_upper', 'N/A')}
        """
        
        st.markdown(stats_text)
    
    with tab3:
        st.markdown("### Trend Interpretation")
        
        interpretation = f"""
        #### Basic Findings:
        - The {selected_metric} shows a **{trend_analysis.get('trend', 'unknown').lower()}** trend over the analysis period.
        - For every year that passes, {selected_metric} changes by approximately **{trend_analysis.get('slope', 0)}** units.
        - Per decade, this translates to a change of **{trend_analysis.get('slope_per_decade', 0)}** units.
        
        #### Statistical Quality:
        - The linear model explains **{float(trend_analysis.get('r_squared', 0)) * 100:.1f}%** of the observed variation in the data.
        - The trend is **{'statistically significant' if float(trend_analysis.get('p_value', 1)) < 0.05 else 'not statistically significant'}** 
          (p-value = {trend_analysis.get('p_value', 'N/A')}).
        
        #### Confidence:
        - We can be 95% confident that the true slope lies between 
          **{trend_analysis.get('ci_lower', 'N/A')}** and **{trend_analysis.get('ci_upper', 'N/A')}**.
        
        #### Implications:
        {"" if trend_analysis.get('trend') == 'Increasing' else ""}
        {
            'The increasing trend suggests that the variable is changing significantly over time, which could have important implications for climate analysis.' 
            if trend_analysis.get('trend') == 'Increasing' else 
            'The decreasing trend is notable for climate analysis purposes.'
        }
        """
        
        st.markdown(interpretation)

else:
    st.error("Unable to load trend analysis data.")
    st.info("Please ensure the backend is running on http://localhost:8000")
