import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy import stats
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

class ClimateAnalytics:
    
    @staticmethod
    def load_data(file_path: str) -> pd.DataFrame:
        df = pd.read_csv(file_path)
        return df
    
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        # Convert time column to datetime and extract year
        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'])
            df['Year'] = df['time'].dt.year
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['Year'])
        
        # Handle missing values using interpolation only for numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].interpolate(method='linear')
        
        # Remove any remaining NaN values
        df = df.dropna()
        
        return df
    
    @staticmethod
    def aggregate_yearly(df: pd.DataFrame) -> pd.DataFrame:
        # Group by year and calculate averages for weather data
        weather_columns = ['temperature_2m', 'relative_humidity_2m', 'precipitation', 'wind_speed_10m']
        available_columns = [col for col in weather_columns if col in df.columns]
        
        if available_columns:
            yearly_avg = df.groupby('Year')[available_columns].mean().reset_index()
        else:
            yearly_avg = df.groupby('Year').mean().reset_index()
        
        return yearly_avg
    
    @staticmethod
    def trend_analysis(df: pd.DataFrame, column: str) -> Dict:
        X = df['Year'].values.reshape(-1, 1)
        y = df[column].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Calculate R-squared
        r_squared = model.score(X, y)
        
        # Calculate p-value
        n = len(X)
        y_pred = model.predict(X)
        residuals = y - y_pred
        se = np.sqrt(np.sum(residuals**2) / (n - 2))
        se_slope = se / np.sqrt(np.sum((X.flatten() - np.mean(X.flatten()))**2))
        t_stat = model.coef_[0] / se_slope
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 2))
        
        # Calculate confidence interval
        confidence_level = 0.95
        degrees_of_freedom = n - 2
        t_critical = stats.t.ppf((1 + confidence_level) / 2, degrees_of_freedom)
        margin_error = t_critical * se_slope
        ci_lower = model.coef_[0] - margin_error
        ci_upper = model.coef_[0] + margin_error
        
        return {
            'slope': round(model.coef_[0], 4),
            'intercept': round(model.intercept_, 2),
            'r_squared': round(r_squared, 4),
            'p_value': round(p_value, 6),
            'trend': 'Increasing' if model.coef_[0] > 0 else 'Decreasing',
            'ci_lower': round(ci_lower, 4),
            'ci_upper': round(ci_upper, 4),
            'slope_per_decade': round(model.coef_[0] * 10, 4)
        }
    
    @staticmethod
    def detect_anomalies(df: pd.DataFrame, column: str, threshold: float = 2) -> List[Dict]:
        values = df[column].values
        mean = np.mean(values)
        std = np.std(values)
        
        anomalies = []
        for idx, row in df.iterrows():
            z_score = (row[column] - mean) / std
            is_anomaly = abs(z_score) > threshold
            
            anomalies.append({
                'year': int(row['Year']),
                'value': round(row[column], 3),
                'is_anomaly': bool(is_anomaly),
                'z_score': round(z_score, 3),
                'severity': 'High' if abs(z_score) > 3 else 'Moderate' if abs(z_score) > 2 else 'Low'
            })
        
        return anomalies
    
    @staticmethod
    def correlation_analysis(df: pd.DataFrame) -> Dict:
        # Use available weather columns for correlation analysis
        weather_columns = ['temperature_2m', 'relative_humidity_2m', 'precipitation', 'wind_speed_10m']
        available_columns = [col for col in weather_columns if col in df.columns]
        
        correlations = {}
        
        # Calculate correlations between available weather variables
        for i, col1 in enumerate(available_columns):
            for j, col2 in enumerate(available_columns):
                if i < j:  # Avoid duplicate correlations
                    try:
                        corr_value = round(df[col1].corr(df[col2]), 3)
                        # Handle NaN values
                        if pd.isna(corr_value):
                            corr_value = 0.0
                        correlation_key = f"{col1}_{col2}"
                        correlations[correlation_key] = corr_value
                    except:
                        correlations[f"{col1}_{col2}"] = 0.0
        
        # Add interpretation
        interpretations = {}
        for key, value in correlations.items():
            if abs(value) > 0.7:
                interpretations[key] = 'Strong correlation'
            elif abs(value) > 0.4:
                interpretations[key] = 'Moderate correlation'
            else:
                interpretations[key] = 'Weak correlation'
        
        return {**correlations, 'interpretations': interpretations}
    
    @staticmethod
    def forecast_temperature(df: pd.DataFrame, years_ahead: int = 10) -> List[Dict]:
        # Use temperature_2m if available, otherwise use first numeric column
        temp_column = 'temperature_2m' if 'temperature_2m' in df.columns else df.select_dtypes(include=[np.number]).columns[0]
        
        X = df['Year'].values.reshape(-1, 1)
        y = df[temp_column].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        last_year = df['Year'].max()
        forecast_years = list(range(last_year + 1, last_year + years_ahead + 1))
        forecast_values = model.predict(np.array(forecast_years).reshape(-1, 1))
        
        # Calculate prediction intervals
        n = len(X)
        y_pred_train = model.predict(X)
        residuals = y - y_pred_train
        mse = np.sum(residuals**2) / (n - 2)
        se_pred = np.sqrt(mse * (1 + 1/n + (np.array(forecast_years) - np.mean(X.flatten()))**2 / np.sum((X.flatten() - np.mean(X.flatten()))**2)))
        
        confidence_level = 0.95
        degrees_of_freedom = n - 2
        t_critical = stats.t.ppf((1 + confidence_level) / 2, degrees_of_freedom)
        
        return [{
            'year': int(year), 
            'predicted_temp': round(temp, 2),
            'ci_lower': round(temp - t_critical * se_pred[i], 2),
            'ci_upper': round(temp + t_critical * se_pred[i], 2)
        } for i, (year, temp) in enumerate(zip(forecast_years, forecast_values))]
    
    @staticmethod
    def calculate_metrics(df: pd.DataFrame) -> Dict:
        # Use temperature_2m if available, otherwise use first numeric column
        temp_column = 'temperature_2m' if 'temperature_2m' in df.columns else df.select_dtypes(include=[np.number]).columns[0]
        
        first_temp = df[temp_column].iloc[0]
        last_temp = df[temp_column].iloc[-1]
        total_increase = last_temp - first_temp
        
        # Calculate decade-wise changes
        decades = df[df['Year'] % 10 == 0].copy()
        if len(decades) > 1:
            decade_changes = []
            for i in range(1, len(decades)):
                change = decades[temp_column].iloc[i] - decades[temp_column].iloc[i-1]
                decade_changes.append(change)
            avg_decade_change = np.mean(decade_changes)
            max_decade_change = max(decade_changes) if decade_changes else 0
            recent_decade_change = decade_changes[-1] if decade_changes else 0
        else:
            avg_decade_change = max_decade_change = recent_decade_change = 0
        
        return {
            'total_temp_increase': round(total_increase, 2),
            'avg_decade_change': round(avg_decade_change, 2),
            'max_decade_change': round(max_decade_change, 2),
            'recent_decade_change': round(recent_decade_change, 2),
            'current_temp': round(last_temp, 2),
            'historical_avg': round(df[temp_column].mean(), 2),
            'max_temp': round(df[temp_column].max(), 2),
            'min_temp': round(df[temp_column].min(), 2)
        }