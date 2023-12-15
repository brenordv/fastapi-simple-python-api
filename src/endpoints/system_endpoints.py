from fastapi import APIRouter

from sys_mon.sys_mon_utils import get_system_status
from utils.env import is_mqtt_configured, is_system_monitor_configured


def configure_system_endpoints(prefix):
    _system_endpoints = APIRouter(prefix=prefix, tags=["System"])

    @_system_endpoints.get("/health", status_code=200,
                           summary="Returns a string 'ping? pong!' to indicate the server is up and running.")
    async def health():
        """
        Health check endpoint.

        :return: Status code 200 if healthy.
        """
        return "ping? pong!"

    if is_mqtt_configured() and is_system_monitor_configured():
        @_system_endpoints.get("/sys-stats", status_code=200,
                               summary="Returns the server status.")
        async def read_sys_stats():
            """
            Reads the system statistics.

            :return: The system status.
            """
            return get_system_status()

    return _system_endpoints
