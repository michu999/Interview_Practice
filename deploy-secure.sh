#!/bin/bash
# Complete deployment with ngrok - ONE command for secure deployment

echo "Starting Secure Deployment with ngrok"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check for NGROK_AUTHTOKEN
if [ -z "$NGROK_AUTHTOKEN" ]; then
    echo "Error: NGROK_AUTHTOKEN not set"
    echo ""
    echo "Run this first:"
    echo "  export NGROK_AUTHTOKEN=your_token_here"
    echo ""
    exit 1
fi

echo "ngrok auth token found"
echo ""

# Step 1: Build and start Django
echo "Step 1: Building Django application..."
docker stop django_travel_blog 2>/dev/null || true
docker rm django_travel_blog 2>/dev/null || true

docker build -t django_travel_blog:latest .

if [ $? -ne 0 ]; then
    echo "Build failed. Check errors above."
    exit 1
fi

# Create database file
touch db.sqlite3

echo "Step 2: Starting Django container..."
docker run -d \
    --name django_travel_blog \
    -p 8000:8000 \
    -v "$(pwd)/db.sqlite3:/app/db.sqlite3" \
    --env-file .env \
    django_travel_blog:latest

if [ $? -ne 0 ]; then
    echo "Failed to start Django. Check: docker logs django_travel_blog"
    exit 1
fi

echo "Django app started"
echo "Waiting for Django to be ready..."
sleep 10

# Step 2: Start ngrok
echo ""
echo "Step 3: Starting ngrok tunnel..."

docker stop ngrok_tunnel 2>/dev/null || true
docker rm ngrok_tunnel 2>/dev/null || true

docker run -d \
    --name ngrok_tunnel \
    --network host \
    -e NGROK_AUTHTOKEN=${NGROK_AUTHTOKEN} \
    ngrok/ngrok http 8000

echo "⏳ Waiting for ngrok to connect..."
sleep 8

# Get ngrok URL
NGROK_URL=""
for i in {1..10}; do
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o '"public_url":"https://[^"]*' | cut -d'"' -f4 | head -1)
    if [ ! -z "$NGROK_URL" ]; then
        break
    fi
    sleep 2
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DEPLOYMENT COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ ! -z "$NGROK_URL" ]; then
    echo "PUBLIC URL:"
    echo "   $NGROK_URL"
    echo ""
    echo "Admin Access:"
    echo "   $NGROK_URL/admin"
    echo "   Username: admin"
    echo "   Password: admin123"
    echo ""
    echo "Create AI Posts:"
    echo "   $NGROK_URL/ai/add/"
else
    echo "Could not auto-detect ngrok URL"
    echo "Visit: http://localhost:4040 to get your URL"
fi

echo "Monitor traffic: http://localhost:4040"
echo "View logs: docker logs -f django_travel_blog"
echo "Stop everything: ./stop-ngrok.sh"


