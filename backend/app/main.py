from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import pandas as pd
import os

from .analytics import ClimateAnalytics

app = FastAPI(title="Climate Change Trends API", version="1.0.0")

# CORS middleware for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data on startup
DATA_FILE = "data/global_temperature.csv"
df = None

@app.on_event("startup")
async def startup_event():
    global df
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = ClimateAnalytics.clean_data(df)
        print(f"Data loaded: {len(df)} records from {df['Year'].min()} to {df['Year'].max()}")
    else:
        print(f"Warning: Data file {DATA_FILE} not found")

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Climate Change Trends API", "status": "running"}

@app.get("/api/climate-data")
def get_climate_data():
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    return df.to_dict('records')

@app.get("/api/summary-stats")
def get_summary_stats():
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    stats = ClimateAnalytics.calculate_metrics(df)
    return stats

@app.get("/api/trend-analysis/{column}")
def get_trend_analysis(column: str):
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    valid_columns = ['Global_Temp', 'CO2_Levels', 'Sea_Level_Rise']
    if column not in valid_columns:
        raise HTTPException(status_code=400, detail=f"Invalid column. Choose from {valid_columns}")
    
    trend = ClimateAnalytics.trend_analysis(df, column)
    return trend

@app.get("/api/anomalies/{column}")
def get_anomalies(column: str, threshold: float = 2):
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    valid_columns = ['Global_Temp', 'CO2_Levels', 'Sea_Level_Rise']
    if column not in valid_columns:
        raise HTTPException(status_code=400, detail=f"Invalid column. Choose from {valid_columns}")
    
    anomalies = ClimateAnalytics.detect_anomalies(df, column, threshold)
    return {"anomalies": anomalies, "total_anomalies": sum(1 for a in anomalies if a['is_anomaly'])}

@app.get("/api/correlations")
def get_correlations():
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    correlations = ClimateAnalytics.correlation_analysis(df)
    return correlations

@app.get("/api/forecast")
def get_forecast(years: int = 10):
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    forecast = ClimateAnalytics.forecast_temperature(df, years)
    return {"forecast": forecast}

@app.get("/api/generate-report")
def generate_report():
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    temp_trend = ClimateAnalytics.trend_analysis(df, 'Global_Temp')
    co2_trend = ClimateAnalytics.trend_analysis(df, 'CO2_Levels')
    sea_trend = ClimateAnalytics.trend_analysis(df, 'Sea_Level_Rise')
    correlations = ClimateAnalytics.correlation_analysis(df)
    anomalies = ClimateAnalytics.detect_anomalies(df, 'Global_Temp')
    metrics = ClimateAnalytics.calculate_metrics(df)
    
    report = {
        "temperature_trend": temp_trend,
        "co2_trend": co2_trend,
        "sea_level_trend": sea_trend,
        "correlations": correlations,
        "anomaly_count": sum(1 for a in anomalies if a['is_anomaly']),
        "total_years": len(df),
        "temp_increase": metrics['total_temp_increase'],
        "current_temp": metrics['current_temp'],
        "historical_avg": metrics['historical_avg'],
        "avg_decade_change": metrics['avg_decade_change']
    }
    
    return report