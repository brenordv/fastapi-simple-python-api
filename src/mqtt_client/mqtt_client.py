import json
import logging
import time

import paho.mqtt.client as mqtt
from simple_log_factory.log_factory import log_factory

from utils.env import MQTT_CLIENT_NAME, MQTT_HOST, MQTT_PORT, is_mqtt_configured


class MQTTClientSingleton:
    __instance = None
    __client = None
    __logger = None

    def __init__(self,
                 client_name: str = MQTT_CLIENT_NAME,
                 host: str = MQTT_HOST,
                 port: int = MQTT_PORT):
        self.__logger = log_factory(client_name, log_level=logging.DEBUG)
        if MQTTClientSingleton.__instance is None:
            __logger = log_factory(client_name)
            MQTTClientSingleton.__instance = self
            # Initialize MQTT client here
            self.__client = mqtt.Client(client_name)

            self.__client.on_connect = self.on_connect
            self.__client.on_message = self.on_message
            self.__client.on_disconnect = self.on_disconnect
            self.__client.on_publish = self.on_publish

            if not is_mqtt_configured():
                return

            try:
                self.__client.connect(host, port, 60)
            except Exception as e:
                __logger.error(f"Failed to connect to MQTT broker. Exception: {e}")

    def reconnect(self):
        attempt = 1
        while not self.__client.is_connected():
            try:
                self.__logger.info(f"Attempting to reconnect (Attempt {attempt})...")
                self.__client.reconnect()
                time.sleep(min(60, 5 * attempt))  # Wait 5 seconds, increasing each attempt, max 60 seconds
            except Exception as e:
                self.__logger.error(f"Reconnect failed: {e}")
                time.sleep(min(60, 5 * attempt))
                attempt += 1
            else:
                self.__logger.info("Reconnected to MQTT Broker")
                break  # Exit the loop after successful reconnection

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.__logger.info("Connected to MQTT Broker!")
        else:
            self.__logger.error(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        self.__logger.info(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    def on_disconnect(self, client, userdata, rc):
        self.__logger.info("Disconnected from MQTT Broker")

    def on_publish(self, client, userdata, mid):
        self.__logger.info(f"Message {mid} is published")

    def publish_to_topic(self, topic, message):
        if not is_mqtt_configured():
            return

        try:
            if not self.__client.is_connected():
                self.reconnect()

            ret = self.__client.publish(topic, message)
            if ret.rc != mqtt.MQTT_ERR_SUCCESS:
                self.__logger.error(f"Publish error: {mqtt.error_string(ret.rc)}")
        except Exception as e:
            self.__logger.error(f"Failed to publish message. Exception: {e}")

    def send_info(self, msg):
        self.publish_to_topic("/alerts/info", msg)

    def send_error_report(self, msg):
        self.publish_to_topic("/alerts/error-reporting", json.dumps(msg))
