# Stage 1: Builder
FROM python:3.13-slim AS builder

# Create app directory
RUN mkdir /app
WORKDIR /app

# Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install OS dependencies + Node.js
RUN apt-get update && apt-get install -y curl build-essential \
 && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
 && apt-get install -y nodejs \
 && apt-get clean

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
RUN apt-get update && apt-get install -y netcat-openbsd && \
    useradd -m -r appuser && \
    mkdir -p /app && mkdir -p /app/logs && mkdir -p /app/staticfiles && \
    chown -R appuser /app

WORKDIR /app

# Copy Python and Node build artifacts from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /app /app

# Ensure directories exist for Django logging and static files
RUN mkdir -p /app/logs /app/staticfiles && chown -R appuser /app/logs /app/staticfiles

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Entrypoint
COPY entrypoint.sh /app/
ENTRYPOINT ["/app/entrypoint.sh"]

USER appuser

EXPOSE 8000



# # Stage 1: Builder
# FROM python:3.13-slim AS builder

# # Create app directory
# RUN mkdir /app
# WORKDIR /app

# # Python env variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Install OS deps for Python + Node
# RUN apt-get update && apt-get install -y curl build-essential \
#  && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
#  && apt-get install -y nodejs \
#  && apt-get clean

# # Install Python deps
# COPY requirements.txt /app/
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# # Install Node deps and build Tailwind CSS (before full code copy)
# COPY package*.json /app/
# RUN npm install

# # Copy full app code
# COPY . /app/

# # Build static assets
# RUN npm run build

# # Collect Django static files
# # RUN python manage.py collectstatic --noinput

# # Stage 2: Runtime
# FROM python:3.13-slim

# # Add netcat and app user
# RUN apt-get update && apt-get install -y netcat-openbsd && \
#     useradd -m -r appuser && \
#     mkdir /app && \
#     chown -R appuser /app

# WORKDIR /app

# COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
# COPY --from=builder /usr/local/bin/ /usr/local/bin/
# COPY --from=builder /app /app

# RUN mkdir -p /app/staticfiles && chown -R appuser /app/staticfiles

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# COPY entrypoint.sh /app/
# ENTRYPOINT ["/app/entrypoint.sh"]

# USER appuser

# EXPOSE 8000

