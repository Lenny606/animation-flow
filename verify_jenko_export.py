import requests
import json

url = "http://localhost:8000/jenko/export"

try:
    print("Testing GET /jenko/export...")
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total items found: {len(data)}")
        if len(data) > 0:
            print("First item preview:")
            print(json.dumps(data[0], indent=2))
    else:
        print("Error Response:")
        print(response.text)
except Exception as e:
    print(f"Request failed: {e}")
