# About the project
This is a simple project I created to showcase some basic functionality of FastAPI, and because I got tired of searching
for reliable and free ways of working with PDF files, especially because the files contained some sensitive information.

I created this, so it would work fine in my home lab setup, but anyone can use it (at least the PDF endpoints).

It comes with docker support to make it easier to use. In the docker image, the port used is `6006`, and if you run it
locally, it's port `8000`. I changed the swagger address to `/api/docs` (so, `http://localhost:8000/api/docs`).


## Endpoints
1. `GET '/api/v1/health'`: Health check endpoint. Returns 200 if the service is up and running.
2. `GET '/api/v1/sys-mon'`: Returns the system's CPU and memory usage.
3. `POST '/api/v1/notify'`: If the request body contains a `msg` field, a message will be sent to the `/alerts/info` MQTT queue.
4. `POST '/v1/error-report/:app_name'`: If the request body contains a `msg` field, a message will be sent to the `/alerts/error-reporting` MQTT queue. 
5. `POST /api/v1/pdf/compress'`: Compresses a PDF file. The file must be sent as a form-data field named `file`.
6. `POST /api/v1/pdf/split'`: Splits a PDF file. The file must be sent as a form-data field named `file`.
7. `POST /api/v1/pdf/merge'`: Merges multiple PDF files.
8. `GET '/api/v1/news/'`: The latest news headlines for Canada.
9. `GET '/api/v1/glucose/latest'`: Returns the latest glucose value registered.
10. `GET '/api/v1/glucose/time-series'`: Gets a time series of glucose values.
11. `GET '/api/v1/glucose/daily-report'`: Returns the latest daily report.
12. `GET '/api/v1/glucose/projections'`: Creates a projection of glucose values for the next 3 hours.

> Some endpoints will not be available, depending on your configuration. PDF endpoints are always available.


## Docker image
In the docker folder there's a Dockerfile that can be used to build the image.
I also provided two scripts:
1. `build.sh`: Builds the image, exposing port `6006`.
2. `run.sh`: Runs the image, configuring all endpoints. It will expose the port `6006`.
3. `run_pdf_only.sh`: Runs the image, but only the PDF endpoints will be available. It will expose the port `6006`.

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

## Note
Starting from version `1.1.0`, if you don't configure MQTT or the required paths, the API will work normally, but will
hide the unavailable endpoints. This is a bit hacky, but will make for a better experience, in case anyone else wants
to use this.
