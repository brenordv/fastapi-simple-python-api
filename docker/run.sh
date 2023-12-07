#!/bin/bash
docker run \
  -d \
  --name myapi \
  -p 6006:6006 \
  --restart unless-stopped \
  -e LOCAL_DISK_PATH=/my/local \
  -e NAS_PATH=/my/nas \
  -e MQTT_HOST=my.mqtt.host \
  myapi