#!/bin/bash
# One-time server setup — run on fresh Ubuntu server
# Usage: sudo bash scripts/setup-server.sh

set -e

echo "=== University Server Setup ==="

# 1. System update
apt update && apt upgrade -y

# 2. Install Docker
curl -fsSL https://get.docker.com | sh

# 3. Install Docker Compose plugin
apt install -y docker-compose-plugin

# 4. Create project directory
mkdir -p /opt/uniguide
cp -r /home/university/uniguide/* /opt/uniguide/

# 5. Setup firewall (ufw)
apt install -y ufw
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw --force enable

# 6. Setup SSH key-only authentication (disable password)
echo "IMPORTANT: Before disabling password auth, ensure SSH key is set up!"
echo "Run: ssh-copy-id university@$(hostname -I | awk '{print $1}')"
echo "Then edit /etc/ssh/sshd_config: PasswordAuthentication no"
echo "Then: systemctl restart sshd"

# 7. Create .env from example
cp /opt/uniguide/.env.example /opt/uniguide/.env
echo "Edit /opt/uniguide/.env with actual values!"

# 8. Build and start
cd /opt/uniguide
docker compose build
docker compose up -d

echo "=== Setup complete! ==="
echo "Next steps:"
echo "1. Edit /opt/uniguide/.env with real passwords and API keys"
echo "2. Setup DNS: A record for guide.hu.edu.af → $(hostname -I | awk '{print $1}')"
echo "3. Install SSL: certbot certonly --webroot -w /opt/uniguide/nginx/html -d guide.hu.edu.af"
echo "4. Copy certs to /opt/uniguide/nginx/certs/"
echo "5. Run: docker compose restart nginx"
