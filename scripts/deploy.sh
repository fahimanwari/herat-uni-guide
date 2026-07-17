#!/bin/bash
# Deploy script — run on the university server
# Usage: bash scripts/deploy.sh

set -e

echo "=== Herat University Guide — Deploy ==="

# 1. Pull latest code
echo "Pulling latest code..."
cd /opt/uniguide
git pull origin main

# 2. Build and restart containers
echo "Building and restarting containers..."
docker compose down
docker compose build --no-cache
docker compose up -d

# 3. Wait for database
echo "Waiting for database..."
sleep 10

# 4. Run migrations
echo "Running migrations..."
docker compose exec api alembic upgrade head

# 5. Health check
echo "Running health check..."
sleep 5
if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API is healthy!"
else
    echo "❌ API health check failed!"
    exit 1
fi

# 6. Backup current database (pre-deploy snapshot)
echo "Creating pre-deploy backup..."
BACKUP_DIR="/opt/uniguide/backups"
mkdir -p "$BACKUP_DIR"
BACKUP_FILE="$BACKUP_DIR/pre-deploy-$(date +%Y%m%d-%H%M%S).sql"
docker compose exec -T db pg_dump -U uniguide uniguide > "$BACKUP_FILE"
echo "Backup saved: $BACKUP_FILE"

echo "=== Deploy complete! ==="
echo "Site: https://guide.hu.edu.af"
echo "API:  https://guide.hu.edu.af/api/v1/health"
