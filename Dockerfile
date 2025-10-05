# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire app folder
COPY app/ app/

# Expose port
EXPOSE 5000

# Set Python path so 'app' module is recognized
ENV PYTHONPATH=/app

# Run the Flask app
CMD ["python", "app/__init__.py"]