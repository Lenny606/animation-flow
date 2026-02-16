import requests
import json
import time

url_post = "http://localhost:8000/jenko/"
url_export = "http://localhost:8000/jenko/export"

filename = f"duplicate_test_{int(time.time())}.avif"

print(f"Testing with filename: {filename}")

# 1. Post first version
print("Posting version 1...")
p1 = {"filename": filename, "title": "Version 1", "category": "Test"}
requests.post(url_post, json=p1)

time.sleep(1)

# 2. Post second version (newest)
print("Posting version 2...")
p2 = {"filename": filename, "title": "Version 2 (Newest)", "category": "Test"}
requests.post(url_post, json=p2)

# 3. Export and verify
print("\nExporting data...")
response = requests.get(url_export)
data = response.json()

matches = [item for item in data if item["filename"] == filename]

print(f"Total entries found with filename '{filename}': {len(matches)}")
if len(matches) == 1:
    print("SUCCESS: Only one entry returned.")
    print(f"Title in export: {matches[0]['title']}")
    if matches[0]['title'] == "Version 2 (Newest)":
        print("SUCCESS: Newest version selected.")
    else:
        print("FAILURE: Wrong version selected.")
else:
    print(f"FAILURE: Expected 1 match, found {len(matches)}.")
    print(json.dumps(matches, indent=2))
