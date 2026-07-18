# 🚀 راهنمای استقرار — Herat University Smart Guide

## پیش‌نیازها
- سرور Ubuntu 22.04+ با حداقل 4GB RAM
- Docker و Docker Compose نصب شده
- دامنه `guide.hu.edu.af` با DNS به IP سرور

## مراحل استقرار

### ۱. نصب Docker (اگر نصب نیست)
```bash
curl -fsSL https://get.docker.com | sh
sudo apt install -y docker-compose-plugin
```

### ۲. کپی فایل‌ها به سرور
```bash
# از مکان محلی
scp -r /home/anwari/Documents/projects/un user@server:/opt/uniguide

# یا از GitHub
ssh user@server
cd /opt
git clone https://github.com/your-repo/un.git uniguide
```

### ۳. تنظیم محیط
```bash
cd /opt/uniguide
cp .env.example .env
nano .env   # مقادیر واقعی را وارد کنید
```

### ۴. ساخت تصاویر Docker
```bash
docker compose build
```

### ۵. راه‌اندازی
```bash
docker compose up -d
```

### ۶. اجرای Migration
```bash
docker compose exec api alembic upgrade head
```

### ۷. ایجاد ادمین
```bash
docker compose exec api python seed_admin.py
```

### ۸. تست سلامت
```bash
curl http://localhost:9000/health
# باید {"status":"ok"} برگرداند
```

### ۹. تنظیم Nginx + SSL
```bash
# نصب certbot
sudo apt install -y certbot

# دریافت گواهی SSL
sudo certbot certonly --webroot -w /opt/uniguide/nginx/html -d guide.hu.edu.af

# کپی گواهی‌ها
sudo cp /etc/letsencrypt/live/guide.hu.edu.af/fullchain.pem /opt/uniguide/nginx/certs/
sudo cp /etc/letsencrypt/live/guide.hu.edu.af/privkey.pem /opt/uniguide/nginx/certs/

# ری‌استارت Nginx
docker compose restart nginx
```

### ۱۰. تنظیم Cron برای بکاپ شبانه
```bash
sudo bash scripts/setup-cron.sh
```

### ۱۱. تنظیم تجدید خودکار SSL
```bash
# اضافه کردن به crontab
echo "0 3 * * 1 certbot renew --quiet && docker compose -f /opt/uniguide/docker-compose.yml restart nginx" | sudo crontab -
```

## آدرس‌ها بعد از استقرار
- **سایت اصلی:** https://guide.hu.edu.af
- **پنل ادمین:** https://guide.hu.edu.af/admin
- **API Docs:** https://guide.hu.edu.af/docs
- **ایمیل ادمین:** admin@herat-uni.edu.af
- **رمز ادمین:** در فایل `assist/05-admin.txt`

## عیب‌یابی
```bash
# بررسی لاگ‌ها
docker compose logs api
docker compose logs web
docker compose logs nginx

# بررسی وضعیت سرویس‌ها
docker compose ps

# ری‌استارت کل سیستم
docker compose down && docker compose up -d
```
