#!/bin/bash
# Quick deploy script for production
# Usage: bash deploy/quick-deploy.sh

set -e

echo "=== Herat University Guide — Quick Deploy ==="

# Check if .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Run: cp deploy/.env.production .env && nano .env"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Installing..."
    curl -fsSL https://get.docker.com | sh
fi

# Build and start
echo "Building Docker images..."
docker compose build --no-cache

echo "Starting services..."
docker compose up -d

# Wait for database
echo "Waiting for database..."
sleep 15

# Run migrations
echo "Running database migrations..."
docker compose exec api alembic upgrade head || echo "Warning: Migration may have already been applied"

# Create admin user
echo "Creating admin user..."
docker compose exec api python seed_admin.py || echo "Warning: Admin may already exist"

# Health check
echo "Running health check..."
sleep 5
if curl -sf http://localhost:9000/health > /dev/null 2>&1; then
    echo ""
    echo "✅ Deploy successful!"
    echo ""
    echo "Site: https://guide.hu.edu.af"
    echo "Admin: https://guide.hu.edu.af/admin"
    echo "API: https://guide.hu.edu.af/api/v1/health"
    echo ""
    echo "Next steps:"
    echo "1. Setup SSL: sudo certbot certonly --webroot -w /opt/uniguide/nginx/html -d guide.hu.edu.af"
    echo "2. Setup cron: sudo bash scripts/setup-cron.sh"
    echo "3. Change admin password in admin panel"
else
    echo ""
    echo "❌ Health check failed! Check logs:"
    echo "docker compose logs api"
    exit 1
fi
