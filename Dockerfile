# Stage 1: Builder
FROM python:3.13-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install OS deps for Python + Node
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

# Add netcat and app user
RUN apt-get update && apt-get install -y netcat-openbsd \
 && useradd -m -r appuser \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python and Node build artifacts from builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /app /app

# Prepare directories and set ownership BEFORE switching user
RUN mkdir -p /app/staticfiles /app/logs \
 && chown -R appuser:appuser /app/staticfiles /app/logs \
 && chmod -R 755 /app/staticfiles /app/logs \
 && chmod +x /app/entrypoint.sh

USER appuser


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY entrypoint.sh /app/
ENTRYPOINT ["/app/entrypoint.sh"]

USER appuser

EXPOSE 8000
