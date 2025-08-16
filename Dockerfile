# Stage 1: Builder
FROM python:3.13-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install OS dependencies + Node
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
 && useradd -m -r -u 1000 appuser \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python and Node artifacts
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /app /app

# Remove old staticfiles/logs, create fresh directories
RUN rm -rf /app/staticfiles /app/logs \
 && mkdir -p /app/staticfiles /app/logs \
 && chown -R appuser:appuser /app

# Copy entrypoint and make executable
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to appuser
USER appuser

ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 8000



