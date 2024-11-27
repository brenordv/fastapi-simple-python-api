# Use an official lightweight Python image.
FROM python:3.11-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define environment variables
ENV LOCAL_DISK_PATH=/local
ENV NAS_PATH=/nas
ENV MQTT_HOST=localhost

# Set work directory in container, all the commands will be ran in this directory
WORKDIR /app

# Copy requirements.txt to the container
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install GhostScript
RUN apt-get update && apt-get install -y ghostscript

# Copy the current directory contents into the container at /app
COPY ./src /app

# Copy the .env file to the container at /app
COPY ./.env /app

# Healthcheck instruction
HEALTHCHECK --interval=5m --timeout=3s CMD python /app/healthcheck.py

# Make port 6006 available to the world outside this container
EXPOSE 6006

# Run the command to start uWSGI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6006"]