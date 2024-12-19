from typing import Union

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from utils.env import is_mqtt_configured


class InfoMessage(BaseModel):
    msg: str


class ErrorReportMessage(BaseModel):
    error_message: str
    stack_trace: str
    extras: Union[dict, str] = None


def configure_messaging_endpoints(prefix):
    _messaging_endpoints = APIRouter(prefix=prefix, tags=["Messaging"])

    if not is_mqtt_configured():
        return None

    from mqtt_client.mqtt_client import MQTTClientSingleton

    client = MQTTClientSingleton()

    @_messaging_endpoints.post(
        "/notify",
        status_code=201,
        summary=" Sends a notification message over MQTT."
    )
    async def notify(payload: InfoMessage):
        """
        Sends a notification message over MQTT.
    
        :param payload: Object with a prop called msg, which contains the actual message.
        :return: Status code 201 if successful.
        """
        client.send_info(payload.msg)
        return

    @_messaging_endpoints.post(
        "/error-report/{app_name}",
        status_code=201,
        summary=" Sends an error report message over MQTT."
    )
    async def error_report(app_name: str, payload: ErrorReportMessage):
        """
        Sends a notification message over MQTT.

        :param app_name: The name of the app that is reporting the error.
        :param payload: Object with a prop called msg, which contains the actual message.
        :return: Status code 201 if successful.
        """
        if not app_name.strip():
            raise HTTPException(status_code=400, detail="App name cannot be empty.")

        if payload is None or all([prop is None for prop in [payload.error_message, payload.stack_trace]]):
            raise HTTPException(status_code=400, detail="Payload cannot be empty.")

        client.send_error_report({
            "app_name": app_name,
            "error_message": payload.error_message,
            "stack_trace": payload.stack_trace,
            "extras": payload.extras
        })
        return

    return _messaging_endpoints
