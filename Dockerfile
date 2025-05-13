# Use official Python image
FROM python:3.12-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies and build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential default-libmysqlclient-dev gcc pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies in a virtualenv to leverage Docker cache
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt

# Copy only the application code (after dependencies for better cache)
FROM python:3.12-slim
WORKDIR /app

# Copy virtualenv from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install runtime dependencies only
RUN apt-get update \
    && apt-get install -y --no-install-recommends default-libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create static directory and set permissions before switching user
RUN mkdir -p /app/static && chown -R appuser:appuser /app

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

# Copy project files
COPY --chown=appuser:appuser . /app/

# Expose port 8000
EXPOSE 8000

# Default command (overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 