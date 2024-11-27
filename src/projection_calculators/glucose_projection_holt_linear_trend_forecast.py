from typing import List

import numpy as np

# Reading delay = 5 minutes in Linux Timestamp
timestamp_reading_delay = 300000


def create_glucose_reading_forecast(
        data: List[int],
        most_recent_timestamp: int,
        min_value: int = 0,
        max_value: int = 450) -> list:
    forecast = holt_linear_trend_forecast(data)

    adjusted_forecast = []
    for index, value in enumerate(forecast):
        adjusted_value = int(max(min(value, max_value), min_value))
        item = {
            "timestamp": most_recent_timestamp + (timestamp_reading_delay * (index + 1)),
            "value": adjusted_value
        }
        adjusted_forecast.append(item)

    return adjusted_forecast


def holt_linear_trend_forecast(data, alpha=0.3, beta=0.1, num_forecasts=36):
    """
    Performs Holt's Linear Trend Method forecasting.

    Parameters:
    - data: list of dictionaries with keys 'timestamp', 'value', 'delta', 'threshold'
    - alpha: smoothing parameter for the level (float between 0 and 1)
    - beta: smoothing parameter for the trend (float between 0 and 1)
    - num_forecasts: number of future periods to forecast

    Returns:
    - forecasts: list of forecasted values
    """
    # Extract the 'value' field from the data
    if isinstance(data, dict):
        values = np.array([entry['value'] for entry in data])
    else:
        values = np.array(data)

    # Initialize level and trend arrays
    L = np.zeros(len(values))
    T = np.zeros(len(values))

    # Initialization
    L[0] = values[0]
    T[0] = values[1] - values[0]  # Initial trend estimate

    # Apply Holt's Linear Trend Method
    for t in range(1, len(values)):
        L[t] = alpha * values[t] + (1 - alpha) * (L[t - 1] + T[t - 1])
        T[t] = beta * (L[t] - L[t - 1]) + (1 - beta) * T[t - 1]

    # Forecast future values
    forecasts = []
    last_level = L[-1]
    last_trend = T[-1]
    for m in range(1, num_forecasts + 1):
        forecast = last_level + m * last_trend
        forecasts.append(forecast)

    return forecasts
