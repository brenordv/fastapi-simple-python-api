#!/bin/bash
cp ./Dockerfile ../Dockerfile
cd ..
docker build -t mypi .
rm Dockerfile