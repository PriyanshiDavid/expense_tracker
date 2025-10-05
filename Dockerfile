# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ app/

# Expose Flask port
EXPOSE 5000

# Set Python path so 'app' module is recognized
ENV PYTHONPATH=/app

# Run the Flask app
CMD ["python", "app/__init__.py"]
