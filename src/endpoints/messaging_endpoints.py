from fastapi import APIRouter
from pydantic import BaseModel

from utils.env import is_mqtt_configured


class Message(BaseModel):
    msg: str


def configure_messaging_endpoints(prefix):
    _messaging_endpoints = APIRouter(prefix=prefix, tags=["Messaging"])

    if not is_mqtt_configured():
        return None

    from mqtt_client.mqtt_client import MQTTClientSingleton

    client = MQTTClientSingleton()

    @_messaging_endpoints.post("/notify", status_code=201,
                               summary=" Sends a notification message over MQTT.")
    async def notify(payload: Message):
        """
        Sends a notification message over MQTT.
    
        :param payload: Object with a prop called msg, which contains the actual message.
        :return: Status code 201 if successful.
        """
        client.notify(payload.msg)
        return

    return _messaging_endpoints
