# Use a slim Python image
FROM python:3.11-slim

# Set a working dir
WORKDIR /app

# Install system deps (if any; e.g. git, build-essential)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      gcc libpq-dev curl \
 && rm -rf /var/lib/apt/lists/*

# Copy and install Python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY backend/ /app/

# Expose the port Uvicorn will run on
EXPOSE 8000

# Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]