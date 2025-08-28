# Django Vacation Project Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client \
    gcc \
    python3-dev \
    libpq-dev \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Fix line endings for Windows compatibility
RUN find . -name "*.sh" -exec dos2unix {} \;

# Create directories for static and media files
RUN mkdir -p /app/staticfiles
RUN mkdir -p /app/media

# Make entrypoint script executable
RUN chmod +x /app/docker-entrypoint.sh

# Expose port
EXPOSE 8000

# Run the startup script
ENTRYPOINT ["/app/docker-entrypoint.sh"]
