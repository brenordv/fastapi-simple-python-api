# About the project
This is a simple project I created to showcase some basic functionality of FastAPI.
It comes with docker, so if you want to try, you can access the API 
at `http://localhost:8000/api/docs`.

## Endpoints
1. `GET '/api/v1/health'`: Health check endpoint. Returns 200 if the service is up and running.
2. `GET '/api/v1/sys-mon'`: Returns the system's CPU and memory usage.
3. `POST '/api/v1/notify`: If the request body contains a `msg` field, a message will be sent to the `/alerts/info` 
MQTT queue.
4. `POST /api/v1/pdf/compress`: Compresses a PDF file. The file must be sent as a form-data field named `file`.
5. `POST /api/v1/pdf/split`: Splits a PDF file. The file must be sent as a form-data field named `file`.
6. `POST /api/v1/pdf/merge`: Merges multiple PDF files.


## Docker image
In the docker folder there's a Dockerfile that can be used to build the image.
I also provided two scripts:
1. `build.sh`: Builds the image, exposing port `6006`.
2. `run.sh`: Runs the image. It will expose the port `6006`. 

The run command has some weird volumes set up because the system monitor uses them
to get info from the host. It's all read-only, so it's safe-ish to use.

# To run this without Docker
You'll need to install Ghostscript
1. Windows: https://ghostscript.com/releases/gsdnld.html
2. Linux: `sudo apt-get update && sudo apt-get install -y ghostscript`

and you'll need to set the following environment variables:
1. `MQTT_HOST`: The MQTT broker host. Defaults to `localhost`.
2. `MQTT_PORT`: The MQTT broker port. Defaults to `1883` (optional. Defaults to 1883).
3. `LOCAL_DISK_PATH`: The path to the local disk.
4. `NAS_PATH`: The path to the NAS.

Variables related to MQTT are pretty specific to my setup, so this endpoint won't do anything for anyone else. (sorry about that)
Without 'LOCAL_DISK_PATH' and 'NAS_PATH' the system monitor won't work.

The PDF endpoints will work regardless of the environment variables.
