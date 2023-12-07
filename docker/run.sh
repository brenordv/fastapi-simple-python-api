#!/bin/bash
docker run \
  -d \
  --name myapi \
  -p 6006:6006 \
  --restart unless-stopped \
  -v /proc:/host/proc:ro \
  -v /sys:/host/sys:ro \
  -v /:/host/root:ro \
  -v /etc:/host/etc:ro \
  -v /physical/path/nas:/my/nas:ro \
  -e LOCAL_DISK_PATH=/ \
  -e NAS_PATH=/my/nas \
  -e MQTT_HOST=my.mqtt.host \
  myapi