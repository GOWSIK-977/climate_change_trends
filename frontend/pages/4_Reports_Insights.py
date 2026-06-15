import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from utils.api_client import APIClient

st.set_page_config(
    page_title="Reports & Insights",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Reports & Insights")

st.markdown("""
This page provides comprehensive climate analysis reports and actionable insights based on your data.
""")

# Create tabs for different report sections
tab1, tab2, tab3, tab4 = st.tabs(["Executive Summary", "Trend Report", "Anomalies Report", "Forecast Report"])

with tab1:
    st.subheader("Executive Summary")
    
    with st.spinner("Generating summary..."):
        summary_stats = APIClient.get_summary_stats()
        
        if summary_stats:
            col1, col2, col3, col4 = st.columns(4)
            
            # Display key metrics
            with col1:
                if 'total_temp_increase' in summary_stats:
                    st.metric(
                        "Total Temperature Increase",
                        f"{summary_stats['total_temp_increase']}°C"
                    )
            
            with col2:
                if 'avg_decade_change' in summary_stats:
                    st.metric(
                        "Avg Change per Decade",
                        f"{summary_stats['avg_decade_change']}°C"
                    )
            
            with col3:
                if 'max_decade_change' in summary_stats:
                    st.metric(
                        "Max Decade Change",
                        f"{summary_stats['max_decade_change']}°C"
                    )
            
            with col4:
                if 'recent_decade_change' in summary_stats:
                    st.metric(
                        "Recent Decade Change",
                        f"{summary_stats['recent_decade_change']}°C"
                    )
            
            # Display comprehensive summary
            st.markdown("### Key Findings")
            
            findings = []
            if summary_stats.get('total_temp_increase', 0) > 0:
                findings.append(f"✓ **Temperature Increase**: Global temperatures have increased by {summary_stats['total_temp_increase']}°C over the analysis period.")
            
            if summary_stats.get('avg_decade_change', 0) != 0:
                trend_direction = "rising" if summary_stats['avg_decade_change'] > 0 else "falling"
                findings.append(f"✓ **Trend**: Average decade-wise change shows {trend_direction} trend of {abs(summary_stats['avg_decade_change'])}°C per decade.")
            
            if summary_stats.get('total_anomalies', 0) > 0:
                findings.append(f"⚠ **Anomalies Detected**: {summary_stats['total_anomalies']} significant anomalies identified.")
            
            if findings:
                for finding in findings:
                    st.markdown(finding)
            else:
                st.info("Summary data is being processed. Please run the dashboard first to generate statistics.")

with tab2:
    st.subheader("Trend Analysis Report")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        column_option = st.selectbox(
            "Select metric for trend analysis:",
            ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
            key="trend_column"
        )
    
    with col1:
        pass
    
    with st.spinner("Analyzing trends..."):
        trend_data = APIClient.get_trend_analysis(column_option)
        
        if trend_data:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Slope", f"{trend_data.get('slope', 'N/A')}")
            
            with col2:
                st.metric("R-squared", f"{trend_data.get('r_squared', 'N/A')}")
            
            with col3:
                st.metric("P-value", f"{trend_data.get('p_value', 'N/A')}")
            
            with col4:
                st.metric("Trend", f"{trend_data.get('trend', 'N/A')}")
            
            st.markdown("### Trend Analysis Details")
            
            trend_text = f"""
            **Metric**: {column_option}
            
            **Trend Direction**: {trend_data.get('trend', 'Unknown')}
            
            **Change Rate (per decade)**: {trend_data.get('slope_per_decade', 'N/A')}
            
            **Statistical Significance**: {'Yes' if float(trend_data.get('p_value', 1)) < 0.05 else 'No'} (p-value: {trend_data.get('p_value', 'N/A')})
            
            **Model Fit (R²)**: {trend_data.get('r_squared', 'N/A')} (explains {float(trend_data.get('r_squared', 0)) * 100:.1f}% of variance)
            
            **Confidence Interval (95%)**: [{trend_data.get('ci_lower', 'N/A')}, {trend_data.get('ci_upper', 'N/A')}]
            
            **Interpretation**: 
            - The {column_option} shows a {'statistically significant' if float(trend_data.get('p_value', 1)) < 0.05 else 'non-significant'} {trend_data.get('trend', 'unknown').lower()} trend.
            - The rate of change is {abs(trend_data.get('slope', 0))} units per year.
            - The model explains {float(trend_data.get('r_squared', 0)) * 100:.1f}% of the observed variation.
            """
            
            st.markdown(trend_text)
        else:
            st.warning("No trend data available. Please ensure the backend is running and data is loaded.")

with tab3:
    st.subheader("Anomaly Detection Report")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        column_option_anom = st.selectbox(
            "Select metric for anomaly detection:",
            ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
            key="anomaly_column"
        )
    
    with col3:
        threshold = st.number_input("Z-score threshold:", value=2.0, min_value=1.0, max_value=5.0)
    
    with col1:
        pass
    
    with st.spinner("Detecting anomalies..."):
        anomalies = APIClient.get_anomalies(column_option_anom, threshold)
        
        if anomalies and isinstance(anomalies, dict) and 'anomalies' in anomalies:
            anomaly_list = anomalies['anomalies']
            
            if isinstance(anomaly_list, list) and len(anomaly_list) > 0:
                st.metric("Total Anomalies Detected", len(anomaly_list))
                
                # Filter anomalies by severity
                high_severity = [a for a in anomaly_list if a.get('severity') == 'High']
                moderate_severity = [a for a in anomaly_list if a.get('severity') == 'Moderate']
                
                if high_severity:
                    st.markdown(f"**🔴 High Severity Anomalies**: {len(high_severity)}")
                if moderate_severity:
                    st.markdown(f"**🟡 Moderate Severity Anomalies**: {len(moderate_severity)}")
                
                st.markdown("### Anomalies Details")
                
                # Display anomalies in a table
                anomaly_df = pd.DataFrame(anomaly_list)
                st.dataframe(
                    anomaly_df,
                    use_container_width=True,
                    column_config={
                        'year': st.column_config.NumberColumn("Year", format="%d"),
                        'value': st.column_config.NumberColumn("Value", format="%.3f"),
                        'z_score': st.column_config.NumberColumn("Z-Score", format="%.3f"),
                        'is_anomaly': st.column_config.CheckboxColumn("Is Anomaly"),
                        'severity': st.column_config.TextColumn("Severity")
                    }
                )
                
                # Provide interpretation
                st.markdown("### Interpretation")
                st.markdown("""
                - **High Severity**: Z-score > 3, indicating extreme deviations
                - **Moderate Severity**: Z-score 2-3, indicating significant deviations
                - **Z-Score**: Number of standard deviations from the mean
                """)
            else:
                st.info(f"No anomalies detected with threshold {threshold} for {column_option_anom}")
        else:
            st.warning("No anomaly data available. Please ensure the backend is running and data is loaded.")

with tab4:
    st.subheader("Temperature Forecast Report")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        years_ahead = st.number_input(
            "Years to forecast ahead:",
            value=10,
            min_value=1,
            max_value=50
        )
    
    with col1:
        pass
    
    with st.spinner("Generating forecast..."):
        # Get forecast from API
        try:
            forecast_response = APIClient.get_forecast(years_ahead)
            forecast_data = forecast_response.get('forecast', []) if isinstance(forecast_response, dict) else forecast_response
            
            if forecast_data and isinstance(forecast_data, list) and len(forecast_data) > 0:
                st.markdown(f"### Temperature Forecast (Next {years_ahead} Years)")
                
                # Display forecast in a table
                forecast_df = pd.DataFrame(forecast_data)
                st.dataframe(
                    forecast_df,
                    use_container_width=True,
                    column_config={
                        'year': st.column_config.NumberColumn("Year", format="%d"),
                        'predicted_temp': st.column_config.NumberColumn("Predicted Temp (°C)", format="%.2f"),
                        'ci_lower': st.column_config.NumberColumn("CI Lower (°C)", format="%.2f"),
                        'ci_upper': st.column_config.NumberColumn("CI Upper (°C)", format="%.2f")
                    }
                )
                
                # Add chart visualization
                st.markdown("### Forecast Visualization")
                st.line_chart(
                    data=forecast_df,
                    x='year',
                    y=['predicted_temp', 'ci_lower', 'ci_upper'],
                    use_container_width=True
                )
                
                st.markdown("""
                ### Forecast Information
                - **Predicted Temp**: Linear regression forecast
                - **CI Lower/Upper**: 95% confidence interval bounds
                - The forecast is based on historical trends in the data
                """)
            else:
                st.info("No forecast data generated yet. Please ensure the backend is running and data is loaded.")
        except Exception as e:
            st.error(f"Error fetching forecast: {e}")
            st.info("Please ensure the backend server is running on http://localhost:8000")

# Footer with export options
st.markdown("---")
st.markdown("### Export Options")

export_col1, export_col2 = st.columns(2)

with export_col1:
    if st.button("📥 Export Executive Summary"):
        try:
            summary = APIClient.get_summary_stats()
            if summary:
                report_text = f"""
# Climate Change Analysis - Executive Report
{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## Key Metrics
- Total Temperature Increase: {summary.get('total_temp_increase', 'N/A')}°C
- Average Change per Decade: {summary.get('avg_decade_change', 'N/A')}°C
- Maximum Decade Change: {summary.get('max_decade_change', 'N/A')}°C
- Recent Decade Change: {summary.get('recent_decade_change', 'N/A')}°C

## Methodology
This report was generated using statistical trend analysis, anomaly detection, and linear regression forecasting.
"""
                st.download_button(
                    label="Download Report as Text",
                    data=report_text,
                    file_name="climate_report.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"Error exporting: {e}")

with export_col2:
    if st.button("📈 Export All Charts Data"):
        try:
            climate_data = APIClient.get_climate_data()
            if climate_data:
                df = pd.DataFrame(climate_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Climate Data as CSV",
                    data=csv,
                    file_name="climate_data.csv",
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"Error exporting: {e}")

st.markdown("""
---
**Note**: All reports are generated from real-time data analysis. 
Make sure the backend server is running and data is loaded through the Dashboard page.
""")
