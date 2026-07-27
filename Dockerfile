FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose backend port
EXPOSE 8000

# Run FastAPI app with Uvicorn (supporting dynamic Railway $PORT)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
