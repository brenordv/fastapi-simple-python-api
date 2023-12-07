from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from mqtt_client.mqtt_client import MQTTClientSingleton
from sys_mon.sys_mon_utils import get_system_status

mqtt_cli = MQTTClientSingleton()
app = FastAPI()
api_router = APIRouter(prefix="/api/v1")


class Message(BaseModel):
    msg: str


@api_router.get("/health", status_code=200)
async def health():
    """
    Health check endpoint.

    :return: Status code 200 if healthy.
    """
    return "pong!"


@api_router.get("/sys-stats")
async def read_sys_stats():
    """
    Reads the system statistics.

    :return: The system status.
    """
    return get_system_status()


@api_router.post("/notify", status_code=201)
async def notify(payload: Message):
    global mqtt_cli
    """
    Sends a notification message over MQTT.

    :param msg: The message to send.
    :return: Status code 201 if successful.
    """
    mqtt_cli.notify(payload.msg)
    return

# Include the APIRouter in the main FastAPI app
app.include_router(api_router)
