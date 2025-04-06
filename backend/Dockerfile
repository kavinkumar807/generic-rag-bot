# Use official Python image
FROM python:3.10-slim AS base

# Set the working directory inside the container
WORKDIR /app

# Copy `requirements.txt` from the root folder
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code into the container
COPY backend /app

# Expose port
EXPOSE 8001

# Run FastAPI
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
