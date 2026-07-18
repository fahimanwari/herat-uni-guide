# 📊 راهنمای مانیتورینگ — Herat University Guide

## ۱. UptimeRobot (رایگان)

### ثبت‌نام
1. به https://uptimerobot.com بروید
2. حساب رایگان بسازید
3. Add New Monitor:
   - **Monitor Type:** HTTP(s)
   - **Friendly Name:** Herat University Guide
   - **URL:** `https://guide.hu.edu.af/api/v1/health`
   - **Monitoring Interval:** 5 minutes
4. اعلان‌ها را روی ایمیل تنظیم کنید

### هشدارهای پیشنهادی
| هشدار | شرط | اقدام |
|-------|------|-------|
| سایت پایین است | ۳ بار متوالی fails | بررسی Docker + Nginx |
| API پاسخ نمی‌دهد | health check fail | بررسی logs + DB |
| SSL منقضی شده | < ۷ روز | certbot renew |

## ۲. Google Search Console

### ثبت دامنه
1. به https://search.google.com/search-console بروید
2. Property جدید اضافه کنید: `guide.hu.edu.af`
3. روش تایید: **HTML tag** — کد زیر را به `layout.tsx` اضافه کنید:

```tsx
// در <head> layout.tsx
<meta name="google-site-verification" content="YOUR_VERIFICATION_CODE" />
```

### ارسال Sitemap
- URL: `https://guide.hu.edu.af/sitemap.xml`
- در Search Console → Sitemaps → Add → Submit

### صفحات کلیدی برای ایندکس
1. صفحه اصلی ( priority: 1)
2. صفحات رشته‌ها ( priority: 0.8)
3. صفحه کانکور آزمایشی ( priority: 0.9)
4. صفحه ماشین حساب چانس ( priority: 0.9)

## ۳. Umami Analytics (خودمیزبان)

### نصب
```bash
# اضافه کردن به docker-compose.yml
umami:
  image: ghcr.io/umami-software/umami:postgresql-latest
  environment:
    DATABASE_URL: postgresql://uniguide:${DB_PASSWORD}@db:5432/uniguide
    APP_SECRET: CHANGE_ME_RANDOM_STRING
  ports:
    - "127.0.0.1:3000:3000"
  depends_on:
    - db
```

### تنظیم در سایت
```tsx
// layout.tsx — اضافه کردن اسکریپت آنالیتیکس
<Script
  defer
  data-website-id="YOUR_UMAMI_WEBSITE_ID"
  src="https://analytics.guide.hu.edu.af/script.js"
/>
```

### داشبورد پیشنهادی
- صفحات پربازدید
- منبع ترافیک (Google vs direct vs social)
- دستگاه (mobile vs desktop)
- کشورهای بازدیدکننده

## ۴. مانیتورینگ سرور

### اسکریپت چک سلامت
```bash
#!/bin/bash
# scripts/health-check.sh — اجرا با cron هر ۱۵ دقیقه

SERVICES=("api:9000" "web:4000")
for svc in "${SERVICES[@]}"; do
    name="${svc%%:*}"
    port="${svc##*:}"
    if curl -sf "http://localhost:$port/health" > /dev/null 2>&1; then
        echo "✅ $name is healthy"
    else
        echo "❌ $name is DOWN! Restarting..."
        docker compose restart "$name"
    fi
done
```

### چک دیسک و RAM
```bash
# اضافه کردن به crontab
0 */6 * * * /opt/uniguide/scripts/server-stats.sh >> /var/log/uniguide-stats.log 2>&1
```

```bash
#!/bin/bash
# scripts/server-stats.sh
echo "=== $(date) ==="
echo "Disk:"
df -h / | tail -1
echo "Memory:"
free -h | grep Mem
echo "Docker:"
docker compose -f /opt/uniguide/docker-compose.yml ps --format "table {{.Name}}\t{{.Status}}"
```

## ۵. اعلان خودکار (اختیاری)

### ایمیل هشدار
```bash
# اضافه کردن به backup.sh یا health-check.sh
if [ $ERROR_COUNT -gt 0 ]; then
    echo "Health check failed at $(date)" | mail -s "Herat Uni Guide Alert" admin@herat-uni.edu.af
fi
```

### تلگرام بات (اختیاری)
```bash
# ارسال پیام به کانال تلگرام
curl -s "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="⚠️ سایت پوهنتون هرات از کار افتاد!"
```
