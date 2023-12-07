# About the project
This is a simple project I created to showcase some basic functionality of FastAPI.
It comes with docker, so if you want to try, you can access the API 
at `http://localhost:8000/docs`.

## Endpoints
1. `GET '/api/v1/sys-mon'`: Returns the system's CPU and memory usage.
2. `POST '/api/v1/notify`: If the request body contains a `msg` field, a message will be sent to the `/alerts/info` 
MQTT queue.
3. `GET '/api/v1/health'`: Health check endpoint. Returns 200 if the service is up and running.


## Docker image
In the docker folder there's a Dockerfile that can be used to build the image.
I also provided two scripts:
1. `build.sh`: Builds the image, exposing port `6006`.
2. `run.sh`: Runs the image. It will expose the port `6006`. 
