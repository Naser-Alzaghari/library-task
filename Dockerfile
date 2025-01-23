# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Install pipenv and required system packages
RUN apt-get update && apt-get install -y libpq-dev gcc && pip install pipenv

# Set the working directory in the container
WORKDIR /app

# Copy Pipfile and Pipfile.lock first to leverage Docker cache
COPY Pipfile Pipfile.lock /app/

# Install dependencies
RUN pipenv install --system --deploy

# Copy the rest of the application's source code
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
