#!/bin/bash
# Setup cron jobs for the project
# Run: sudo bash scripts/setup-cron.sh

set -e

echo "=== Setting up cron jobs ==="

# Nightly backup at 2 AM
CRON_LINE="0 2 * * * /opt/uniguide/scripts/backup.sh >> /var/log/uniguide-backup.log 2>&1"

# Check if already exists
if crontab -l 2>/dev/null | grep -q "uniguide/scripts/backup.sh"; then
    echo "Backup cron job already exists"
else
    (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
    echo "Added nightly backup cron job (2 AM daily)"
fi

# Verify
echo "Current crontab:"
crontab -l 2>/dev/null | grep uniguide || echo "  (no uniguide jobs)"

echo "=== Cron setup complete ==="
echo "Backup logs: /var/log/uniguide-backup.log"
