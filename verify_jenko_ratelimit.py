import requests
import time

url = "http://localhost:8000/jenko/"

payload = {
  "filename": "ratelimit_test.avif",
  "title": "Rate Limit Test",
  "category": "Test"
}

print("Testing rate limit (5 requests per minute allowed)...")

for i in range(1, 8):
    try:
        response = requests.post(url, json=payload)
        print(f"Request {i}: Status Code: {response.status_code}")
        if response.status_code == 429:
            print("SUCCESS: Rate limit reached (Status 429).")
            break
        elif response.status_code != 200:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request {i} failed: {e}")

if i < 7 and response.status_code == 429:
    print("\nRate limiting is working correctly.")
else:
    print("\nRate limiting FAILED or not reached.")
