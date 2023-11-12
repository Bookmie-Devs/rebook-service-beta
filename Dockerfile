# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.11-slim-buster    

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir -p /app

# Set the working directory to /music_service
WORKDIR /app

# Copy the current directory contents into the container at /music_service
COPY . /app/

RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "python","manage.py","runserver","8000"]