import os

mqtt_client_name: str = os.environ.get("MQTT_CLIENT_NAME", "MQTTClient")
mqtt_host: str = os.environ.get("MQTT_HOST")
mqtt_port: int = int(os.environ.get("MQTT_PORT", "1883"))
local_disk_path: str = os.environ.get("LOCAL_DISK_PATH")
nas_path: str = os.environ.get("NAS_PATH")


def is_mqtt_configured():
    global mqtt_client_name, mqtt_host, mqtt_port
    return mqtt_client_name is not None and mqtt_host is not None and mqtt_port is not None


def is_system_monitor_configured():
    """
    Checks if the system monitor is configured.
    Remark: This should also check for the volumes, but the environment variables are fine for now.
    """
    global local_disk_path, nas_path
    return local_disk_path is not None and nas_path is not None
