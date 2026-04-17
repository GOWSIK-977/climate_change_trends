import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000/api"

class APIClient:
    
    @staticmethod
    def get_climate_data():
        try:
            response = requests.get(f"{API_BASE_URL}/climate-data")
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"Connection error: {e}")
            return []
    
    @staticmethod
    def get_summary_stats():
        try:
            response = requests.get(f"{API_BASE_URL}/summary-stats")
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            st.error(f"Connection error: {e}")
            return {}
    
    @staticmethod
    def get_trend_analysis(column):
        try:
            response = requests.get(f"{API_BASE_URL}/trend-analysis/{column}")
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            st.error(f"Connection error: {e}")
            return {}
    
    @staticmethod
    def get_anomalies(column, threshold=2):
        try:
            response = requests.get(f"{API_BASE_URL}/anomalies/{column}", params={"threshold": threshold})
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            st.error(f"Connection error: {e}")
            return {}
    
    @staticmethod
    def get_correlations():
        try:
            response = requests.get(f"{API_BASE_URL}/correlations")
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            st.error(f"Connection error: {e}")
            return {}
    
    @staticmethod
    def get_forecast(years=10):
        try:
            response = requests.get(f"{API_BASE_URL}/forecast", params={"years": years})
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            st.error(f"Connection error: {e}")
            return {}
    
    @staticmethod
    def generate_report():
        try:
            response = requests.get(f"{API_BASE_URL}/generate-report")
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            st.error(f"Connection error: {e}")
            return {}