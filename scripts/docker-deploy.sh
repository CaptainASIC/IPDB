#!/bin/bash

# Docker deployment script for IP Tracker
# This script builds and runs the IP Tracker application using Docker Compose

set -e

echo "🚀 Starting IP Tracker deployment with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. You can modify it if needed."
fi

# Build and start services
echo "🔨 Building and starting services..."
if command -v docker-compose &> /dev/null; then
    docker-compose down --remove-orphans
    docker-compose build --no-cache
    docker-compose up -d
else
    docker compose down --remove-orphans
    docker compose build --no-cache
    docker compose up -d
fi

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
if command -v docker-compose &> /dev/null; then
    if docker-compose ps | grep -q "Up"; then
        echo "✅ Services are running successfully!"
    else
        echo "❌ Some services failed to start. Check logs with: docker-compose logs"
        exit 1
    fi
else
    if docker compose ps | grep -q "running"; then
        echo "✅ Services are running successfully!"
    else
        echo "❌ Some services failed to start. Check logs with: docker compose logs"
        exit 1
    fi
fi

echo ""
echo "🎉 IP Tracker is now running!"
echo "📱 Access the application at: http://localhost:8501"
echo "🗄️  PostgreSQL is available at: localhost:5432"
echo ""
echo "📋 Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Restart services: docker-compose restart"
echo ""

