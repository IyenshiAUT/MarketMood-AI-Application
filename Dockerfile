# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ./app/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code into the container
COPY ./app/api/ ./api/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run uvicorn to start the API.
# The `uvicorn` command points to the main.py file within the `api` folder.
# The environment variables for MLflow are passed during the `docker run` command at deployment.
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]