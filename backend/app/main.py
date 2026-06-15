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
DATA_FILE = "c:\\Users\\gowsik\\Documents\\PROJECT SEM 4\\climate-change-trends\\data\\TNweather_1.8M.csv"
FALLBACK_FILE = "c:\\Users\\gowsik\\Documents\\PROJECT SEM 4\\climate-change-trends\\data\\global_temperature.csv"
DATA_SOURCE_NAME = "TNweather_1.8M.csv"
df = None

@app.on_event("startup")
async def startup_event():
    global df
    file_to_load = None
    source_name = DATA_SOURCE_NAME
    
    if os.path.exists(DATA_FILE):
        file_to_load = DATA_FILE
    elif os.path.exists(FALLBACK_FILE):
        file_to_load = FALLBACK_FILE
        source_name = "global_temperature.csv"
    
    if file_to_load:
        df = pd.read_csv(file_to_load)
        df = ClimateAnalytics.clean_data(df)
        print(f"Data loaded: {len(df)} records from {df['Year'].min()} to {df['Year'].max()}")
        print(f"Data Source: {source_name}")
    else:
        print(f"Warning: Data file not found. Tried {DATA_FILE} and {FALLBACK_FILE}")

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Climate Change Trends API", "status": "running"}

@app.get("/api/data-source")
def get_data_source():
    if df is None:
        return {"data_source": "Unknown", "status": "not loaded"}
    return {
        "data_source": DATA_SOURCE_NAME,
        "file_path": DATA_FILE,
        "total_records": len(df),
        "year_range": f"{int(df['Year'].min())} - {int(df['Year'].max())}"
    }

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
    
    valid_columns = ['temperature_2m', 'relative_humidity_2m', 'precipitation', 'wind_speed_10m']
    if column not in valid_columns:
        raise HTTPException(status_code=400, detail=f"Invalid column. Choose from {valid_columns}")
    
    trend = ClimateAnalytics.trend_analysis(df, column)
    return trend

@app.get("/api/anomalies/{column}")
def get_anomalies(column: str, threshold: float = 2):
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    valid_columns = ['temperature_2m', 'relative_humidity_2m', 'precipitation', 'wind_speed_10m']
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
    
    temp_trend = ClimateAnalytics.trend_analysis(df, 'temperature_2m')
    humidity_trend = ClimateAnalytics.trend_analysis(df, 'relative_humidity_2m')
    precip_trend = ClimateAnalytics.trend_analysis(df, 'precipitation')
    wind_trend = ClimateAnalytics.trend_analysis(df, 'wind_speed_10m')
    correlations = ClimateAnalytics.correlation_analysis(df)
    anomalies = ClimateAnalytics.detect_anomalies(df, 'temperature_2m')
    metrics = ClimateAnalytics.calculate_metrics(df)
    
    report = {
        "temperature_trend": temp_trend,
        "humidity_trend": humidity_trend,
        "precipitation_trend": precip_trend,
        "wind_trend": wind_trend,
        "correlations": correlations,
        "anomaly_count": sum(1 for a in anomalies if a['is_anomaly']),
        "total_years": len(df),
        "temp_increase": metrics['total_temp_increase'],
        "current_temp": metrics['current_temp'],
        "historical_avg": metrics['historical_avg'],
        "avg_decade_change": metrics['avg_decade_change']
    }
    
    return report