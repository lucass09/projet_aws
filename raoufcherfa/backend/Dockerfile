# Use an official Python runtime as the base image
FROM python:3.8.3-alpine

# Set the working directory in the container to /app
RUN pip install --upgrade pip

RUN adduser -D myuser
USER myuser
WORKDIR /home/myuser

# Copy the current directory contents into the container at /app
COPY --chown=myuser:myuser . /app

# Install the required packages
RUN pip install --user --no-cache-dir --no-warn-script-location -r /app/requirements.txt

ENV PATH="/home/myuser/.local/bin:${PATH}"

# Expose port 8081 to the host machine
EXPOSE 8081

# Run the command to start the Flask app
CMD [ "python", "/app/main.py" ]