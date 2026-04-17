import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class APIClient:
    """Climate data API client"""
    
    @staticmethod
    def get_climate_data():
        """Load climate data"""
        years = list(range(1880, 2024))
        
        # Generate realistic climate data
        np.random.seed(42)
        
        # Temperature data (increasing trend)
        base_temp = 13.5
        temp_increase = 0.008  # 0.8°C per century
        temp_noise = 0.15
        global_temp = [base_temp + (y - 1880) * temp_increase + np.random.normal(0, temp_noise) 
                      for y in years]
        
        # CO2 levels (accelerating)
        co2_levels = [280 + (y - 1880) * 0.5 + (y - 1880)**2 * 0.005 + np.random.normal(0, 2)
                     for y in years]
        
        # Sea level rise
        sea_level = [0 + (y - 1880) * 0.8 + (y - 1880)**2 * 0.01 + np.random.normal(0, 5)
                    for y in years]
        
        data = []
        for i, year in enumerate(years):
            data.append({
                'Year': year,
                'Global_Temp': round(global_temp[i], 2),
                'CO2_Levels': round(co2_levels[i], 1),
                'Sea_Level_Rise': round(sea_level[i], 1)
            })
        
        return data
    
    @staticmethod
    def get_summary_stats():
        """Get summary statistics"""
        data = APIClient.get_climate_data()
        df = pd.DataFrame(data)
        
        return {
            'total_temp_increase': round(df['Global_Temp'].iloc[-1] - df['Global_Temp'].iloc[0], 2),
            'current_temp': round(df['Global_Temp'].iloc[-1], 2),
            'recent_decade_change': round(df['Global_Temp'].iloc[-1] - df['Global_Temp'].iloc[-11], 2)
        }
    
    @staticmethod
    def get_correlations():
        """Calculate correlations between variables"""
        data = APIClient.get_climate_data()
        df = pd.DataFrame(data)
        
        temp_co2_corr = df['Global_Temp'].corr(df['CO2_Levels'])
        temp_sea_corr = df['Global_Temp'].corr(df['Sea_Level_Rise'])
        co2_sea_corr = df['CO2_Levels'].corr(df['Sea_Level_Rise'])
        
        def interpret_corr(corr):
            if abs(corr) > 0.7:
                return "Strong correlation"
            elif abs(corr) > 0.5:
                return "Moderate correlation"
            elif abs(corr) > 0.3:
                return "Weak correlation"
            else:
                return "Negligible correlation"
        
        return {
            'temp_co2': round(temp_co2_corr, 3),
            'temp_sea': round(temp_sea_corr, 3),
            'co2_sea': round(co2_sea_corr, 3),
            'interpretations': {
                'temp_co2': interpret_corr(temp_co2_corr),
                'temp_sea': interpret_corr(temp_sea_corr),
                'co2_sea': interpret_corr(co2_sea_corr)
            }
        }
    
    @staticmethod
    def get_trend_analysis(metric):
        """Perform trend analysis on a metric"""
        data = APIClient.get_climate_data()
        df = pd.DataFrame(data)
        
        x = df['Year'].values
        y = df[metric].values
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Calculate confidence intervals
        n = len(x)
        se_slope = std_err / np.sqrt(np.sum((x - np.mean(x))**2))
        t_critical = stats.t.ppf(0.975, n-2)
        ci_lower = slope - t_critical * se_slope
        ci_upper = slope + t_critical * se_slope
        
        return {
            'trend': "Increasing" if slope > 0 else "Decreasing",
            'slope': round(slope, 4),
            'slope_per_decade': round(slope * 10, 4),
            'r_squared': round(r_value**2, 4),
            'p_value': round(p_value, 6),
            'ci_lower': round(ci_lower, 4),
            'ci_upper': round(ci_upper, 4)
        }
    
    @staticmethod
    def get_anomalies(metric, threshold=2.0):
        """Detect anomalies using Z-score method"""
        data = APIClient.get_climate_data()
        df = pd.DataFrame(data)
        
        mean_val = df[metric].mean()
        std_val = df[metric].std()
        
        anomalies = []
        for _, row in df.iterrows():
            z_score = (row[metric] - mean_val) / std_val
            is_anomaly = abs(z_score) > threshold
            
            severity = "High" if abs(z_score) > 2.5 else "Medium" if abs(z_score) > 2.0 else "Low"
            
            anomalies.append({
                'year': int(row['Year']),
                'value': round(row[metric], 2),
                'z_score': round(z_score, 2),
                'is_anomaly': bool(is_anomaly),
                'severity': severity if is_anomaly else None
            })
        
        total_anomalies = sum(1 for a in anomalies if a['is_anomaly'])
        
        return {
            'total_anomalies': total_anomalies,
            'anomalies': anomalies
        }
    
    @staticmethod
    def generate_report():
        """Generate comprehensive report"""
        data = APIClient.get_climate_data()
        df = pd.DataFrame(data)
        
        temp_trend = APIClient.get_trend_analysis('Global_Temp')
        sea_trend = APIClient.get_trend_analysis('Sea_Level_Rise')
        anomalies = APIClient.get_anomalies('Global_Temp', 2.0)
        
        return {
            'temp_increase': round(df['Global_Temp'].iloc[-1] - df['Global_Temp'].iloc[0], 2),
            'temperature_trend': temp_trend,
            'sea_level_trend': sea_trend,
            'anomaly_count': anomalies['total_anomalies']
        }
    
    @staticmethod
    def get_forecast(years=10):
        """Generate temperature forecast"""
        data = APIClient.get_climate_data()
        df = pd.DataFrame(data)
        
        # Use recent 50 years for forecasting
        recent_df = df.tail(50)
        x = recent_df['Year'].values
        y = recent_df['Global_Temp'].values
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        last_year = df['Year'].iloc[-1]
        forecast_years = list(range(int(last_year) + 1, int(last_year) + years + 1))
        
        # Calculate prediction intervals
        x_mean = np.mean(x)
        n = len(x)
        
        forecasts = []
        for year in forecast_years:
            predicted = slope * year + intercept
            
            # Confidence interval calculation
            se_pred = std_err * np.sqrt(1 + 1/n + (year - x_mean)**2 / np.sum((x - x_mean)**2))
            t_critical = stats.t.ppf(0.975, n-2)
            ci_lower = predicted - t_critical * se_pred
            ci_upper = predicted + t_critical * se_pred
            
            forecasts.append({
                'year': year,
                'predicted_temp': round(predicted, 2),
                'ci_lower': round(ci_lower, 2),
                'ci_upper': round(ci_upper, 2)
            })
        
        return {'forecast': forecasts}
