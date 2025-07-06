FROM python:3.11-slim

WORKDIR /app

# Install deps
COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit app
COPY frontend/ /app/

# Expose Streamlit port
EXPOSE 8501

# Start Streamlit
CMD ["streamlit", "run", "about.py", "--server.address=0.0.0.0", "--server.port=8501"]