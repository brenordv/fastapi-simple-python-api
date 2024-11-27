import os
from typing import TypedDict, Optional
from dotenv import load_dotenv

possible_env_places = ["./src/.env", "./.env"]
for env_place in possible_env_places:
    if os.path.exists(env_place):
        load_dotenv(env_place)
        break


class GlucoseReadingConfig(TypedDict):
    base_url: Optional[str]
    api_code: Optional[str]

CORS_ALLOWED_ORIGINS: str = os.environ.get("CORS_ALLOWED_ORIGINS", "*")

MQTT_CLIENT_NAME: str = os.environ.get("MQTT_CLIENT_NAME", "MQTTClient")
MQTT_HOST: str = os.environ.get("MQTT_HOST")
MQTT_PORT: int = int(os.environ.get("MQTT_PORT", "1883"))
LOCAL_DISK_PATH: str = os.environ.get("LOCAL_DISK_PATH")
NAS_PATH: str = os.environ.get("NAS_PATH")
API_KEY: str = os.environ.get("GLOBAL_NS_API_KEY")
LATEST_GLUCOSE_READING_API_CONFIG: GlucoseReadingConfig = {
    "base_url": os.environ.get("BASE_LATEST_GLUCOSE_READING_URL"),
    "api_code": os.environ.get("API_CODE_LATEST_GLUCOSE_READING"),
}
GLUCOSE_TIME_SERIES_API_CONFIG: GlucoseReadingConfig = {
    "base_url": os.environ.get("BASE_GLUCOSE_TIMESERIES_URL"),
    "api_code": os.environ.get("API_CODE_GLUCOSE_TIME_SERIES"),
}
DAILY_REPORT_API_CONFIG: GlucoseReadingConfig = {
    "base_url": os.environ.get("BASE_DAILY_REPORT_URL"),
    "api_code": os.environ.get("API_CODE_DAILY_REPORT_API"),
}

def is_mqtt_configured() -> bool:
    """
    Checks if the MQTT client is configured.
    """
    return MQTT_CLIENT_NAME is not None and MQTT_HOST is not None and MQTT_PORT is not None


def is_system_monitor_configured() -> bool:
    """
    Checks if the system monitor is configured.
    Remark: This should also check for the volumes, but the environment variables are fine for now.
    """
    return LOCAL_DISK_PATH is not None and NAS_PATH is not None


def is_glucose_monitor_configured() -> bool:
    """
    Checks if the Glucose Monitor API is configured.
    """
    required_configs = [
        LATEST_GLUCOSE_READING_API_CONFIG,
        GLUCOSE_TIME_SERIES_API_CONFIG,
        DAILY_REPORT_API_CONFIG,
    ]

    if not API_KEY:
        return False

    for config in required_configs:
        if not config.get("base_url") or not config.get("api_code"):
            return False

    return True
