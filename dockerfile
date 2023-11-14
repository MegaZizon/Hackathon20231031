# Use an official Python runtime as a parent image
FROM python:3.11

# Create and set the working directory
WORKDIR /usr/src/app

# Copy the requirements file into the container at /app
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
# Install any needed packages specified in requirements.txt
COPY . /usr/src/app/
# Collect static files
RUN pip install --upgrade pip
RUN pip install -r requirements.txt