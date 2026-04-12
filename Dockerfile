# Stage 1: Build the React frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files and install dependencies
COPY frontend/package*.json ./
RUN npm ci

# Set empty base URL so frontend makes relative API calls to the same host
ENV NEXT_PUBLIC_API_BASE_URL=""

# Copy the rest of the frontend code and build
COPY frontend/ ./
RUN npm run build

# Stage 2: Setup Python backend and serve
FROM python:3.12-slim

WORKDIR /app

# Copy the built frontend from the builder stage
# This will place it at /app/frontend/out, matching the path resolution in main.py
COPY --from=frontend-builder /app/frontend/out /app/frontend/out

# Setup the backend
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .

# Render dynamically assigns a port via the PORT environment variable
ENV PORT=8000
EXPOSE $PORT

# Start the FastAPI server using Uvicorn
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
