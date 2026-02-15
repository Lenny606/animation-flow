#!/bin/bash
set -e

BASE_URL="http://localhost:8000"

echo "1. Signup..."
curl -s -X POST "$BASE_URL/auth/signup" \
    -H "Content-Type: application/json" \
    -d '{"email": "test@example.com", "password": "password123"}' > signup_response.json
cat signup_response.json
echo ""

echo "2. Login..."
TOKEN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=test@example.com&password=password123")
ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access_token": "[^"]*' | grep -o '[^"]*$' )
echo "Token received"

if [ -z "$ACCESS_TOKEN" ]; then
    echo "Login failed!"
    echo $TOKEN_RESPONSE
    exit 1
fi

echo "3. Chat Endpoint..."
curl -s -X POST "$BASE_URL/agent/chat" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -d '{"message": "Hello AI"}' > chat_response.json
cat chat_response.json
echo ""

echo "Verification Complete!"
