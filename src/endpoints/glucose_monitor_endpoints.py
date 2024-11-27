from typing import List

from fastapi import APIRouter, Query

from data_fetcher.glucose_values_fetcher import fetch_latest_glucose_value, TOTAL_RECORDS_24HOURS, \
    fetch_glucose_time_series, fetch_daily_report
from projection_calculators.glucose_projection_holt_linear_trend_forecast import create_glucose_reading_forecast

from utils.env import is_glucose_monitor_configured


def configure_glucose_monitor_endpoints(prefix):
    gm_endpoints = APIRouter(prefix=f"{prefix}/glucose", tags=["Glucose Monitor"])

    if not is_glucose_monitor_configured():
        return None

    @gm_endpoints.get("/latest", status_code=200,
                      summary="Returns the latest glucose value registered.")
    async def latest_glucose_value_endpoint():
        """
        Returns the latest glucose value registered.
        """

        latest_value = fetch_latest_glucose_value()
        return latest_value

    @gm_endpoints.get("/time-series", status_code=200,
                      summary="gets a time series of glucose values.")
    async def time_series_endpoint(
            limit: int = Query(
                description="Number of records to return. Default is 288 (24 hours).", default=TOTAL_RECORDS_24HOURS)):
        """
        Gets a time series of glucose values.

        :argument limit: Number of records to return. Default is 288 (24 hours).
        """
        time_series = fetch_glucose_time_series(limit)
        return time_series

    @gm_endpoints.get("/daily-report", status_code=200,
                      summary="Returns the latest daily report.")
    async def latest_glucose_value_endpoint():
        """
        Returns the latest daily report.
        """

        daily_report = fetch_daily_report()
        return daily_report

    @gm_endpoints.get("/projections", status_code=200,
                      summary="creates a projection of glucose values for the next 3 hours.")
    async def time_series_endpoint(
            past_glucose_values: List[int] = Query(description="Glucose readings for the few hours."),
            most_recent_timestamp: int = Query(description="Most recent timestamp of the glucose readings.")
    ):
        """
        Creates a projection of glucose values for the next 3 hours.

        :argument past_glucose_values: Glucose readings for the few hours.
        :argument most_recent_timestamp: Most recent timestamp of the glucose readings.
        """
        forecast = create_glucose_reading_forecast(past_glucose_values, most_recent_timestamp)
        return forecast

    return gm_endpoints
