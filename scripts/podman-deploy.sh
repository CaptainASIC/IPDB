#!/bin/bash

# Podman deployment script for IP Tracker
# This script builds and runs the IP Tracker application using Podman

set -e

echo "🚀 Starting IP Tracker deployment with Podman..."

# Check if Podman is installed
if ! command -v podman &> /dev/null; then
    echo "❌ Podman is not installed. Please install Podman first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. You can modify it if needed."
fi

# Create network if it doesn't exist
echo "🌐 Creating Podman network..."
podman network exists ip-tracker-network || podman network create ip-tracker-network

# Create volume for PostgreSQL data
echo "💾 Creating PostgreSQL data volume..."
podman volume exists postgres_data || podman volume create postgres_data

# Stop and remove existing containers
echo "🧹 Cleaning up existing containers..."
podman stop ip-tracker-db ip-tracker-app 2>/dev/null || true
podman rm ip-tracker-db ip-tracker-app 2>/dev/null || true

# Start PostgreSQL container
echo "🗄️  Starting PostgreSQL container..."
podman run -d \
    --name ip-tracker-db \
    --network ip-tracker-network \
    -e POSTGRES_DB=iptracker \
    -e POSTGRES_USER=iptracker \
    -e POSTGRES_PASSWORD=iptracker123 \
    -e POSTGRES_INITDB_ARGS="--encoding=UTF-8" \
    -v postgres_data:/var/lib/postgresql/data \
    -v ./database/schema.sql:/docker-entrypoint-initdb.d/01-schema.sql:Z \
    -v ./database/seeds/sample_data.sql:/docker-entrypoint-initdb.d/02-sample_data.sql:Z \
    -p 5432:5432 \
    postgres:15-alpine

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 15

# Build application image using Podman-specific Dockerfile
echo "🔨 Building application image..."
podman build -f Dockerfile.podman -t ip-tracker-app .

# Start application container
echo "📱 Starting application container..."
podman run -d \
    --name ip-tracker-app \
    --network ip-tracker-network \
    -e DATABASE_URL=postgresql://iptracker:iptracker123@ip-tracker-db:5432/iptracker \
    -e STREAMLIT_SERVER_PORT=8501 \
    -e STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    -v ./app:/app:Z \
    -p 8501:8501 \
    ip-tracker-app

# Wait for application to be ready
echo "⏳ Waiting for application to be ready..."
sleep 10

# Check if containers are running
if podman ps | grep -q "ip-tracker-db" && podman ps | grep -q "ip-tracker-app"; then
    echo "✅ Services are running successfully!"
else
    echo "❌ Some services failed to start. Check logs with: podman logs <container-name>"
    exit 1
fi

echo ""
echo "🎉 IP Tracker is now running!"
echo "📱 Access the application at: http://localhost:8501"
echo "🗄️  PostgreSQL is available at: localhost:5432"
echo ""
echo "📋 Useful commands:"
echo "  - View app logs: podman logs -f ip-tracker-app"
echo "  - View db logs: podman logs -f ip-tracker-db"
echo "  - Stop services: podman stop ip-tracker-app ip-tracker-db"
echo "  - Remove services: podman rm ip-tracker-app ip-tracker-db"
echo "  - List containers: podman ps -a"
echo ""

