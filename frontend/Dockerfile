# Use official Python image
FROM python:3.10-slim-bookworm AS base

# Set the working directory inside the container
WORKDIR /app

# Install only Streamlit
RUN pip install --no-cache-dir streamlit python-dotenv

# Copy the frontend code into the container
COPY frontend /app

# Copy the `public` folder into the container
COPY ./public /public

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
