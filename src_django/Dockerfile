FROM python:3.11-slim-buster

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev libpq-dev curl vim \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Create a non-root user
RUN adduser --system --group scoring \
    && chown -R scoring:scoring /app

# Copy project files
COPY pyproject.toml .
COPY poetry.lock .

# Install Poetry
RUN pip install "poetry==1.7.1"

# Expose port 8000
EXPOSE 8000

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only main

# Copy projct code
COPY . .

RUN chmod +x /app/health_check.sh

# Set the entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
