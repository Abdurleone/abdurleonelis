#!/bin/bash
cd /root/abdurleonelis/backend
rm -f lab.db
source /root/abdurleonelis/venv/bin/activate

# Start server in background
python -m uvicorn main:app --host 127.0.0.1 --port 8000 > /tmp/server.log 2>&1 &
SERVER_PID=$!
sleep 3

echo "=== Testing Backend ==="
echo ""
echo "1. Register user..."
REG=$(curl -s -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"tech1","password":"pass123","role":"technician"}')
echo "Response: $REG"
echo ""

echo "2. Login..."
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=tech1&password=pass123" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
echo "Token: $TOKEN" | head -c 50
echo "..."
echo ""

echo "3. Create patient (with auth)..."
PATIENT=$(curl -s -X POST "http://localhost:8000/patients/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","dob":"1990-01-15"}')
echo "Response: $PATIENT"
echo ""

echo "4. List patients (no auth)..."
curl -s -X GET "http://localhost:8000/patients/"
echo ""
echo ""

kill $SERVER_PID
