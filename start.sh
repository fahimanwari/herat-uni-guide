#!/bin/bash
# Start both backend (port 9000) and frontend (port 4000)
# Usage: bash start.sh

DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Killing old servers..."
kill $(lsof -ti:4000) 2>/dev/null || true
kill $(lsof -ti:9000) 2>/dev/null || true
sleep 1

# --- Backend (port 9000) ---
echo ""
echo "=== Backend (port 9000) ==="
cd "$DIR/backend"
source .venv/bin/activate
setsid uvicorn app.main:app --host 0.0.0.0 --port 9000 > /tmp/backend.log 2>&1 &
sleep 3

if ss -tlnp | grep -q ":9000"; then
    echo "✅ Backend running: http://localhost:9000"
else
    echo "❌ Backend failed"
    tail -5 /tmp/backend.log
fi

# --- Frontend (port 4000) ---
echo ""
echo "=== Frontend (port 4000) ==="
cd "$DIR/web"
npx next build 2>&1 | tail -3
setsid node node_modules/.bin/next start -p 4000 > /tmp/frontend.log 2>&1 &
sleep 3

if ss -tlnp | grep -q ":4000"; then
    echo "✅ Frontend running: http://localhost:4000"
else
    echo "❌ Frontend failed"
    tail -5 /tmp/frontend.log
fi

echo ""
echo "========================================="
echo "  Frontend:  http://localhost:4000"
echo "  Backend:   http://localhost:9000"
echo "  Admin:     http://localhost:9000/admin"
echo "  Swagger:   http://localhost:9000/docs"
echo "========================================="
