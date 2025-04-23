# Use a minimal Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock to container
COPY Pipfile .
COPY Pipfile.lock .

# Install dependencies using pipenv directly into the container’s system Python
RUN pipenv install --system --deploy

# Copy the app code
COPY ./app ./app

# Expose the FastAPI default port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
