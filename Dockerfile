# Stage 1: Builder
FROM python:3.13-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install OS dependencies for Python + Node
RUN apt-get update && apt-get install -y curl build-essential \
 && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
 && apt-get install -y nodejs \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install Node dependencies
COPY package*.json /app/
RUN npm install

# Copy full app code
COPY . /app/

# Build static assets
RUN npm run build

# Stage 2: Runtime
FROM python:3.13-slim

# Install netcat and create app user
RUN apt-get update && apt-get install -y netcat-openbsd \
 && useradd -m -r appuser \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python and Node build artifacts from builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
# Copy app code but remove staticfiles to avoid root-owned files
COPY --from=builder /app /app
RUN rm -rf /app/staticfiles

# Prepare directories and set ownership
RUN mkdir -p /app/staticfiles /app/logs \
 && chown -R appuser:appuser /app \
 && chmod -R 755 /app/staticfiles /app/logs \
 && chmod +x /app/entrypoint.sh

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy entrypoint script
COPY entrypoint.sh /app/
ENTRYPOINT ["/app/entrypoint.sh"]

# Run as non-root user
USER appuser

EXPOSE 8000

