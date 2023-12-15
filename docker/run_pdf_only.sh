#!/bin/bash
docker run \
  -d \
  --name myapi \
  -p 6006:6006 \
  --restart unless-stopped \
  myapi