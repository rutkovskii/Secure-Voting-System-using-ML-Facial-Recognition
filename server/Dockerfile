# Use an official Python runtime as the base image
FROM python:3.10-slim-buster

LABEL maintainer="Aleksei Rutkovskii <arutkovskii@umass.edu>"
LABEL version="0.1"
LABEL description="Dockerfile for Secure Voting System — Server"

# Set the working directory to /server
WORKDIR /server

# Copy the requirements file to the container
COPY requirements_server.txt requirements_server.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements_server.txt

RUN pip install gunicorn

# Copy the rest of the application code to the container
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=runner.py

# Expose port 5000 for Flask
EXPOSE 5000

# Set the default command to run when the container starts
CMD ["gunicorn", "-b", "0.0.0.0:5000", "runner:FlaskApp", "--timeout", "90", "--workers", "1"]

# CMD ["tail", "-f", "/dev/null"]