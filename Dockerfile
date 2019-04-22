# Use an official Python runtime as a parent image
FROM python:3.7
# Add all projects file to app directory
ADD . /usr/src/app
# Set app as a working directory
WORKDIR /usr/src/app
# Copy requirement.text to app
COPY requirements.txt ./
# install all dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt
# Expose port 8000 from the container
EXPOSE 8000
# Execute command to run the server
CMD exec gunicorn graphqlDemo.wsgi:application --bind 0.0.0.0:8000 --workers 3