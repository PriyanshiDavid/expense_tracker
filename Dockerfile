# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ app/

# Copy tests so pytest can find them
COPY tests/ tests/

# Expose Flask port
EXPOSE 5000

# Set Python path so 'app' module is recognized
ENV PYTHONPATH=/app

# Set default command to run the Flask app
CMD ["python", "app/__init__.py"]
