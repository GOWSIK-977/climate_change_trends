# 🌍 Climate Change Trends Analysis Platform

A comprehensive full-stack web application for analyzing, visualizing, and forecasting global climate trends using statistical methods, machine learning, and interactive dashboards.

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Project Architecture](#project-architecture)
5. [Project Structure](#project-structure)
6. [Installation & Setup](#installation--setup)
7. [Running the Application](#running-the-application)
8. [API Documentation](#api-documentation)
9. [Feature Explanations](#feature-explanations)
10. [Data Processing Pipeline](#data-processing-pipeline)
11. [Usage Guide](#usage-guide)
12. [Contributing](#contributing)

---

## 🎯 Project Overview

The **Climate Change Trends Analysis Platform** is an advanced analytics system designed to:

- **Analyze** historical climate data from 1880 to 2023
- **Detect** anomalies and extreme weather patterns
- **Forecast** future temperature trends
- **Visualize** complex climate relationships
- **Generate** comprehensive reports with statistical insights

This platform combines real-time data processing, statistical analysis, and interactive visualization to provide actionable insights into global climate patterns.

### 🎓 What This Project Does

1. **Data Ingestion**: Loads climate datasets containing temperature, humidity, precipitation, and wind speed data
2. **Data Cleaning**: Handles missing values, duplicates, and normalizes temporal data
3. **Statistical Analysis**: Performs trend analysis, anomaly detection, and correlation studies
4. **Forecasting**: Uses linear regression to predict future temperature trends
5. **Visualization**: Creates interactive charts and dashboards for easy interpretation
6. **Report Generation**: Produces comprehensive climate analysis reports
7. **Export**: Allows users to download data and reports in multiple formats

---

## ✨ Features

### 🏠 Dashboard
- **Real-time climate metrics** displaying global temperature increases
- **Multi-metric visualization** showing temperature, humidity, precipitation, and wind data
- **Historical trend charts** spanning over 140 years of data
- **Summary statistics** with key performance indicators
- **Data overview** with record counts and temporal range

### 📈 Trend Analysis
- **Linear regression analysis** to identify climate trends
- **Statistical significance testing** using p-values and confidence intervals
- **Trend direction detection** (increasing/decreasing patterns)
- **Decade-wise change calculations** for long-term pattern analysis
- **Model fit metrics** (R-squared) to assess prediction accuracy
- **Interactive visualizations** with trend lines and confidence bands

### ⚠️ Anomaly Detection
- **Z-score based detection** to identify unusual climate events
- **Severity classification** (High/Moderate/Low) based on deviation magnitude
- **Customizable thresholds** for sensitivity adjustments
- **Visual highlighting** of anomalies on trend charts
- **Exportable anomaly reports** with detailed information
- **Historical anomaly tracking** to identify extreme events over time

### 📊 Reports & Insights
- **Executive Summary** with key climate findings
- **Comprehensive trend reports** for each weather metric
- **Anomaly detection reports** with severity analysis
- **Temperature forecasts** for 1-50 years ahead with confidence intervals
- **CSV export functionality** for data analysis
- **Text report generation** for documentation

---

## 🛠️ Technology Stack

### **Backend**
- **Framework**: FastAPI (Python web framework)
- **Data Processing**: Pandas, NumPy
- **Statistical Analysis**: SciPy, Scikit-learn
- **Server**: Uvicorn (ASGI server)

### **Frontend**
- **Framework**: Streamlit (Python-based UI framework)
- **Visualization**: Plotly, Plotly Express
- **HTTP Client**: Requests library

### **Data & Analytics**
- **Linear Regression**: Scikit-learn
- **Statistical Tests**: SciPy stats
- **Data Manipulation**: Pandas
- **Numerical Computing**: NumPy

### **Development Tools**
- **Language**: Python 3.10+
- **Package Manager**: pip
- **Version Control**: Git

---

## 🏗️ Project Architecture

### **System Architecture Diagram**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Climate Analysis Platform                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   Frontend (Streamlit)                    │   │
│  │  ┌────────────┬────────────┬────────────┬────────────┐   │   │
│  │  │ Dashboard  │  Trends    │ Anomalies  │  Reports   │   │   │
│  │  └────────────┴────────────┴────────────┴────────────┘   │   │
│  │         Navigation Sidebar with Page Selection            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            ↕ HTTP                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Backend API (FastAPI)                        │   │
│  │  ┌────────────┬────────────┬────────────┬────────────┐   │   │
│  │  │  Climate   │  Trend     │  Anomaly   │ Forecast   │   │   │
│  │  │  Endpoints │ Analysis   │ Detection  │ Endpoints  │   │   │
│  │  └────────────┴────────────┴────────────┴────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            ↕                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Analytics Engine                             │   │
│  │  ┌────────────┬────────────┬────────────┬────────────┐   │   │
│  │  │  Data      │ Statistical│ Anomaly    │ Forecasting│   │   │
│  │  │ Cleaning   │ Analysis   │ Detection  │ Models     │   │   │
│  │  └────────────┴────────────┴────────────┴────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            ↕                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Data Layer                                   │   │
│  │  ┌────────────────────────────────────────────────────┐   │   │
│  │  │  CSV Files: global_temperature.csv                 │   │   │
│  │  │             TNweather_1.8M.csv                     │   │   │
│  │  └────────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### **Data Flow**

```
Raw Data (CSV)
    ↓
Data Loading & Parsing
    ↓
Data Cleaning (Missing values, Duplicates, Normalization)
    ↓
Aggregation (Yearly averages)
    ↓
Analytics Processing
    ├─→ Trend Analysis (Linear Regression)
    ├─→ Anomaly Detection (Z-score method)
    ├─→ Correlation Analysis
    └─→ Forecasting (Linear Extrapolation)
    ↓
Results Visualization & Export
    ↓
User Interface (Streamlit)
```

---

## 📁 Project Structure

```
climate-change-trends/
│
├── README.md                           # Project documentation (this file)
│
├── backend/                            # FastAPI Backend
│   ├── run.py                         # Application startup script
│   ├── requirements.txt                # Backend dependencies
│   │
│   └── app/
│       ├── __init__.py
│       ├── main.py                    # FastAPI application & routes
│       ├── analytics.py               # Statistical analysis & ML models
│       ├── models.py                  # Data schema definitions
│       ├── schemas.py                 # Request/response schemas
│       ├── database.py                # Database utilities
│       ├── crud.py                    # Database operations
│       │
│       ├── routers/
│       │   ├── __init__.py
│       │   └── climate.py             # Climate-specific routes
│       │
│       └── data/
│           ├── global_temperature.csv # Temperature data
│           ├── raw/                   # Raw data files
│           └── processed/             # Processed data files
│
├── frontend/                           # Streamlit Frontend
│   ├── app.py                         # Main Streamlit app
│   ├── requirements.txt                # Frontend dependencies
│   │
│   ├── pages/
│   │   ├── 1_Dashboard.py            # Dashboard page
│   │   ├── 2_Trend_Analysis.py       # Trend analysis page
│   │   ├── 3_Anomaly_Detection.py    # Anomaly detection page
│   │   └── 4_Reports_Insights.py     # Reports page
│   │
│   └── utils/
│       ├── __init__.py
│       └── api_client.py             # API communication utilities
│
├── data/                              # Data directory
│   ├── global_temperature.csv         # Historical temperature data
│   ├── TNweather_1.8M.csv            # Weather dataset (1.8M records)
│   ├── raw/                           # Raw datasets
│   └── processed/                     # Processed datasets
│
├── notebooks/                         # Jupyter notebooks
│   └── data_analysis.ipynb           # Data exploration & analysis
│
└── reports/                           # Generated reports
    ├── climate_insights_summary.md    # Climate insights
    └── sustainability_recommendations.md
```

---

## 💻 Installation & Setup

### **Prerequisites**
- Python 3.10 or higher
- pip (Python package manager)
- Windows, macOS, or Linux

### **Step 1: Clone/Download Project**

```bash
cd climate-change-trends
```

### **Step 2: Create Virtual Environment (Optional but Recommended)**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### **Step 3: Install Backend Dependencies**

```bash
cd backend
pip install -r requirements.txt
cd ..
```

### **Step 4: Install Frontend Dependencies**

```bash
cd frontend
pip install -r requirements.txt
cd ..
```

### **Backend Requirements** (`backend/requirements.txt`)
```
fastapi==0.104.1
uvicorn==0.24.0
pandas==2.1.1
numpy==1.26.0
scikit-learn==1.3.2
scipy==1.11.3
pydantic==2.4.2
python-multipart==0.0.6
```

### **Frontend Requirements** (`frontend/requirements.txt`)
```
streamlit==1.28.1
pandas==2.1.1
plotly==5.17.0
requests==2.31.0
numpy==1.26.0
```

---

## 🚀 Running the Application

### **Option 1: Start Both Services Manually**

**Terminal 1 - Start Backend (FastAPI)**
```bash
cd backend
python run.py
```
The backend will start on: `http://localhost:8000`

**Terminal 2 - Start Frontend (Streamlit)**
```bash
cd frontend
python -m streamlit run app.py
```
The frontend will start on: `http://localhost:8505` (or `http://localhost:8504`)

### **Option 2: Using Python Directly**

**Terminal 1 - Backend**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend**
```bash
cd frontend
python -m streamlit run app.py
```

### **Verify Services Are Running**

- **Backend Health Check**: Open http://localhost:8000/ in browser
- **Frontend**: Open http://localhost:8505 in browser
- **API Documentation**: Go to http://localhost:8000/docs (Swagger UI)

---

## 📡 API Documentation

### **Base URL**
```
http://localhost:8000/api
```

### **Endpoints**

#### **1. Get Climate Data**
```http
GET /api/climate-data
```
**Response**: Array of climate records with all metrics

```json
[
  {
    "Year": 1880,
    "temperature_2m": 14.52,
    "relative_humidity_2m": 65.3,
    "precipitation": 45.2,
    "wind_speed_10m": 8.5
  }
]
```

---

#### **2. Get Summary Statistics**
```http
GET /api/summary-stats
```
**Response**: Key climate metrics

```json
{
  "total_temp_increase": 1.23,
  "current_temp": 15.75,
  "historical_avg": 14.52,
  "avg_decade_change": 0.18,
  "max_decade_change": 0.35,
  "recent_decade_change": 0.28
}
```

---

#### **3. Trend Analysis**
```http
GET /api/trend-analysis/{column}
```
**Parameters**: 
- `column`: `temperature_2m`, `relative_humidity_2m`, `precipitation`, or `wind_speed_10m`

**Response**: Trend statistics

```json
{
  "slope": 0.0092,
  "intercept": 13.45,
  "r_squared": 0.8234,
  "p_value": 0.000001,
  "trend": "Increasing",
  "ci_lower": 0.0071,
  "ci_upper": 0.0113,
  "slope_per_decade": 0.092
}
```

---

#### **4. Anomaly Detection**
```http
GET /api/anomalies/{column}?threshold=2
```
**Parameters**: 
- `column`: Weather metric column
- `threshold`: Z-score threshold (default: 2)

**Response**: List of anomalies

```json
{
  "anomalies": [
    {
      "year": 1998,
      "value": 16.45,
      "is_anomaly": true,
      "z_score": 2.34,
      "severity": "Moderate"
    }
  ],
  "total_anomalies": 15
}
```

---

#### **5. Correlation Analysis**
```http
GET /api/correlations
```
**Response**: Correlation matrix between weather variables

```json
{
  "temperature_2m_relative_humidity_2m": -0.523,
  "temperature_2m_precipitation": 0.234,
  "interpretations": {
    "temperature_2m_relative_humidity_2m": "Moderate correlation"
  }
}
```

---

#### **6. Temperature Forecast**
```http
GET /api/forecast?years=10
```
**Parameters**: 
- `years`: Number of years to forecast (1-50)

**Response**: Forecasted temperatures with confidence intervals

```json
{
  "forecast": [
    {
      "year": 2024,
      "predicted_temp": 15.89,
      "ci_lower": 15.65,
      "ci_upper": 16.13
    }
  ]
}
```

---

#### **7. Generate Report**
```http
GET /api/generate-report
```
**Response**: Comprehensive climate analysis report

```json
{
  "temperature_trend": { ... },
  "humidity_trend": { ... },
  "precipitation_trend": { ... },
  "wind_trend": { ... },
  "anomaly_count": 15,
  "total_years": 144
}
```

---

## 🔬 Feature Explanations

### **1. Data Cleaning Process**

The `clean_data()` function in `analytics.py`:

```python
1. Temporal Parsing: Converts 'time' column to datetime format
2. Year Extraction: Extracts year from dates
3. Deduplication: Removes duplicate records by year
4. Interpolation: Fills missing numeric values using linear interpolation
5. Null Removal: Drops remaining NaN values
```

**Why?** Ensures consistent, high-quality data for analysis

---

### **2. Trend Analysis (Linear Regression)**

**Method**: Ordinary Least Squares (OLS) Linear Regression

**Formula**: `y = mx + b`
- `m` (slope) = rate of change per year
- `b` (intercept) = baseline value
- `R²` = proportion of variance explained (0-1, higher is better)

**Statistical Testing**:
- **P-value**: Probability that trend is due to chance
  - p < 0.05 = Statistically significant
  - p ≥ 0.05 = Not significant
- **Confidence Interval**: Range where true slope likely lies (95% confidence)

**Example Output**:
```
Temperature slope: 0.0092°C/year
R²: 0.82 (explains 82% of variation)
P-value: 0.000001 (highly significant)
Per decade: 0.092°C increase
```

---

### **3. Anomaly Detection (Z-Score Method)**

**Formula**: `Z = (Value - Mean) / Standard Deviation`

**Interpretation**:
- Z = 0: Value equals mean
- Z = ±1: Within 1 standard deviation (68% normal)
- Z = ±2: Unusual (5% of population)
- Z = ±3: Very unusual (0.3% of population)
- Z = ±4: Extremely rare (0.006% of population)

**Severity Classification**:
- **High**: |Z| > 3 → Extreme events
- **Moderate**: 2 < |Z| ≤ 3 → Unusual events
- **Low**: |Z| ≤ 2 → Normal variation

**Example**: For temperature with mean 15°C and std dev 0.5°C:
- Value 16.5°C → Z = 3.0 → High severity anomaly

---

### **4. Temperature Forecasting**

**Method**: Linear Regression Extrapolation

**Steps**:
1. Fit linear model to historical temperature data
2. Extract slope (rate of change)
3. Project trend forward N years
4. Calculate prediction intervals using residual variance

**Prediction Interval Formula**:
```
PI = Predicted Value ± (t-critical × Standard Error)
```

**Limitations**:
- Assumes linear trend continues
- Does not account for policy changes or abrupt shifts
- More accurate for shorter timeframes
- Confidence widens with longer forecasts

---

### **5. Correlation Analysis**

**Method**: Pearson Correlation Coefficient

**Range**: -1 to +1
- +1 = Perfect positive correlation
- 0 = No correlation
- -1 = Perfect negative correlation

**Interpretation**:
- |r| > 0.7 = Strong correlation
- 0.4 < |r| ≤ 0.7 = Moderate correlation
- |r| ≤ 0.4 = Weak correlation

**Example**: Temperature vs Humidity might show -0.52 (moderate negative correlation)

---

## 📊 Data Processing Pipeline

### **Stage 1: Data Loading**
```python
# Loads CSV files into pandas DataFrame
df = pd.read_csv("TNweather_1.8M.csv")
# Result: DataFrame with 1.8M weather records
```

### **Stage 2: Data Cleaning**
```python
# Temporal normalization
df['Year'] = pd.to_datetime(df['time']).dt.year

# Deduplication by year
df = df.drop_duplicates(subset=['Year'])

# Interpolate missing values
df[numeric_cols] = df[numeric_cols].interpolate(method='linear')

# Remove NaNs
df = df.dropna()
```

### **Stage 3: Aggregation**
```python
# Calculate yearly averages
yearly_data = df.groupby('Year')[weather_cols].mean()
```

### **Stage 4: Analysis**
```python
# Perform statistical analysis on aggregated data
trend = trend_analysis(yearly_data, 'temperature_2m')
anomalies = detect_anomalies(yearly_data, 'temperature_2m')
forecast = forecast_temperature(yearly_data, years_ahead=10)
```

### **Stage 5: Presentation**
```python
# Visualize and export results
# - Interactive charts on Dashboard
# - Statistical details in Trend Analysis
# - Anomaly maps in Anomaly Detection
# - Forecast visualizations in Reports
```

---

## 📖 Usage Guide

### **For Data Analysts**

1. **Explore Dashboard**: Get overview of climate trends
2. **View Trend Analysis**: Understand directional changes with statistics
3. **Analyze Anomalies**: Identify extreme weather events
4. **Export Data**: Download data for further analysis

### **For Climate Researchers**

1. **Access API**: Use endpoints for custom analysis
2. **View Statistical Details**: Review confidence intervals and p-values
3. **Generate Reports**: Create comprehensive climate reports
4. **Compare Metrics**: Use correlation analysis for relationships

### **For Decision Makers**

1. **Read Executive Summary**: Key findings on dashboard
2. **Review Forecasts**: Understand future climate trends
3. **Download Reports**: Share insights with stakeholders
4. **Track Anomalies**: Monitor extreme events

---

## 🧮 Mathematical Foundations

### **Linear Regression**
```
Minimize: Σ(yi - ŷi)²
ŷi = mx + b
m = Σ((xi - x̄)(yi - ȳ)) / Σ((xi - x̄)²)
```

### **Z-Score Standardization**
```
Z = (X - μ) / σ

where:
- X = individual value
- μ = population mean
- σ = standard deviation
```

### **Pearson Correlation**
```
r = Σ((xi - x̄)(yi - ȳ)) / √(Σ(xi - x̄)² × Σ(yi - ȳ)²)
```

---

## 🔧 Advanced Configuration

### **Backend Configuration**

Edit `backend/app/main.py`:
```python
# Data file path
DATA_FILE = "path/to/your/data.csv"

# CORS settings
allow_origins=["*"]  # Allow all origins

# Server settings
host = "0.0.0.0"
port = 8000
```

### **Frontend Configuration**

Edit `frontend/app.py`:
```python
# API Base URL
API_BASE_URL = "http://localhost:8000/api"

# Page layout
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)
```

---

## 📈 Performance Optimization

### **For Large Datasets (>10M records)**

1. **Aggregate data before analysis**:
   ```python
   yearly_avg = df.groupby('Year').mean()
   ```

2. **Use data sampling for visualizations**:
   ```python
   df_sample = df.sample(n=10000)
   ```

3. **Cache API responses** in Streamlit:
   ```python
   @st.cache_data
   def get_climate_data():
       return APIClient.get_climate_data()
   ```

---

## 🐛 Troubleshooting

### **Backend Issues**

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | Change port: `uvicorn app.main:app --port 8001` |
| Module not found | Run `pip install -r requirements.txt` |
| Data file not found | Update DATA_FILE path in main.py |

### **Frontend Issues**

| Issue | Solution |
|-------|----------|
| Cannot connect to backend | Ensure backend is running on port 8000 |
| Missing packages | Run `pip install -r requirements.txt` in frontend folder |
| Pages not showing | Ensure pages are in `frontend/pages/` directory |

---

## 📝 Example Use Cases

### **Case 1: Climate Change Impact Assessment**
1. Open Dashboard to see global temperature increase
2. Go to Trend Analysis to see rate of change per decade
3. Check Anomaly Detection for extreme weather events
4. Export report for presentation

### **Case 2: Forecasting Future Climate**
1. Open Reports & Insights
2. Select Forecast Report tab
3. Adjust forecast period (default: 10 years)
4. Review confidence intervals
5. Download forecast data

### **Case 3: Identifying Climate Extremes**
1. Go to Anomaly Detection
2. Adjust Z-score threshold (2-4 range)
3. Filter by severity level
4. View anomaly visualization
5. Export anomaly list for investigation

---

## 🤝 Contributing

### **To Add New Features**

1. **Backend Enhancement**:
   - Add method to `ClimateAnalytics` class in `analytics.py`
   - Create endpoint in `main.py`
   - Update API documentation

2. **Frontend Enhancement**:
   - Add page in `frontend/pages/`
   - Update `app.py` navigation
   - Update requirements.txt if needed

3. **Testing**:
   - Test with sample data
   - Verify API responses
   - Check visualization rendering

---

## 📚 Resources

- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Scikit-learn**: https://scikit-learn.org/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Streamlit**: https://docs.streamlit.io/

---

## 📄 License

This project is provided as-is for educational and research purposes.

---

## 👤 Author Notes

**Project Purpose**: Demonstrate full-stack data science application development combining:
- Statistical analysis
- Machine learning
- Web APIs
- Interactive dashboards
- Data visualization

**Key Learning Points**:
- Backend-frontend integration
- RESTful API design
- Statistical modeling
- Interactive UI development
- Data processing pipelines

---

## 📞 Support

For issues, questions, or contributions, please refer to the troubleshooting section or review the code comments.

---

**Last Updated**: May 27, 2026
**Version**: 1.0.0
**Status**: Production Ready ✅

