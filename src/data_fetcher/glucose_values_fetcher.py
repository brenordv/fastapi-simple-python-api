from raccoontools.shared.requests_with_retry import post

from utils.env import LATEST_GLUCOSE_READING_API_CONFIG, API_KEY, GLUCOSE_TIME_SERIES_API_CONFIG, \
    DAILY_REPORT_API_CONFIG, GlucoseReadingConfig

TOTAL_RECORDS_24HOURS: int = 288


def _fetch_data(api_config: GlucoseReadingConfig, url_path: str, name: str):
    base_url = api_config.get("base_url")
    if not base_url:
        raise ValueError(f"Base URL for [{name}] is not configured.")

    url = f"{base_url}/{url_path}"

    response = post(
        url,
        json={
            "key": API_KEY
        },
        params={
            "code": api_config.get("api_code")
        })

    return response.json()

def fetch_latest_glucose_value():
    return _fetch_data(LATEST_GLUCOSE_READING_API_CONFIG, "api/DataApiFunc", "Latest Glucose Reading")


def fetch_glucose_time_series(limit: int = TOTAL_RECORDS_24HOURS):
    return _fetch_data(GLUCOSE_TIME_SERIES_API_CONFIG, f"api/DataSeriesApiFunc/{limit}", "Glucose Time Series")


def fetch_daily_report():
    return _fetch_data(DAILY_REPORT_API_CONFIG, "api/DataLatestDailyReportFunc", "Daily Report")
