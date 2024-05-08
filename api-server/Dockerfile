# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV SECRET_KEY="19961217"
ENV DB_USERNAME="dennis_lee"
ENV DB_PASSWORD="popoman1217"
ENV DB_NAME="dennis_lee_crypto"
ENV INSTANCE_CONNECTION_NAME="bold-impulse-421609:us-central1:dennis-lee-project-db-1"

# Run the application
CMD flask run --host=0.0.0.0 --port=${PORT:-8080}

