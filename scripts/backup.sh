#!/bin/bash
# Nightly backup — runs via cron
# Add to crontab: 0 2 * * * /opt/uniguide/scripts/backup.sh
# This backs up the database AND uploads to university cPanel via FTP

set -e

BACKUP_DIR="/opt/uniguide/backups"
DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="$BACKUP_DIR/uniguide-$DATE.sql"
KEEP_DAYS=7

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Dump database
echo "Backing up database..."
docker compose -f /opt/uniguide/docker-compose.yml exec -T db \
    pg_dump -U uniguide uniguide > "$BACKUP_FILE"

# Compress
gzip "$BACKUP_FILE"
COMPRESSED="${BACKUP_FILE}.gz"
echo "Backup created: $COMPRESSED"

# Upload to cPanel via FTP (off-site backup)
# Fill in your cPanel FTP credentials in .env or here
if [ -n "$CPANEL_FTP_HOST" ]; then
    echo "Uploading to cPanel..."
    curl -T "$COMPRESSED" \
        "ftp://$CPANEL_FTP_HOST/backups/uniguide/" \
        --user "$CPANEL_FTP_USER:$CPANEL_FTP_PASS" \
        --ftp-create-dirs
    echo "Upload complete."
else
    echo "Skipping cPanel upload (CPANEL_FTP_HOST not set)"
fi

# Clean old local backups (keep 7 days)
echo "Cleaning old backups..."
find "$BACKUP_DIR" -name "uniguide-*.sql.gz" -mtime +$KEEP_DAYS -delete

echo "=== Backup complete ==="
