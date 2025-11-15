#!/bin/bash
# Stop secure deployment and backup database

echo "🛑 Stopping secure deployment..."
echo ""

# Stop ngrok
echo "Stopping ngrok tunnel..."
docker stop ngrok_tunnel 2>/dev/null || true
docker rm ngrok_tunnel 2>/dev/null || true

# Stop Django
echo "Stopping Django app..."
docker stop django_travel_blog 2>/dev/null || true

# Backup database
if [ -f "db.sqlite3" ]; then
    BACKUP="db_backup_$(date +%Y%m%d_%H%M%S).sqlite3"
    cp db.sqlite3 "$BACKUP"
    echo "💾 Database backed up to: $BACKUP"
fi

echo ""
echo "✅ Everything stopped"
echo "🔒 Your IP is no longer exposed"
echo "💾 Data saved in: db.sqlite3"

