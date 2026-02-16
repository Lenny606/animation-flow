import requests
import json

url = "http://localhost:8000/jenko/"

payload = {
  "filename": "2024-02-15_12-30-45_cyberpunk-city.png",
  "title": "Neon Horizons",
  "description": "A futuristic cityscape at dusk with flying cars.",
  "medium": "Digital Art",
  "year": "2024",
  "tags": [
    "cyberpunk", 
    "scifi",
    "neon"
  ],
  "width": 1024,
  "height": 1024,
  "id": "optional_mongo_id", 
  "src": "https://example.com/image.png"
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
    else:
        print("Error Response:")
        print(response.text)
except Exception as e:
    print(f"Request failed: {e}")
