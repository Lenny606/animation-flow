import urllib.request
import json

def verify():
    url = "http://localhost:8000/jenko/"
    payload = {
        "filename": "test_image.jpg",
        "title": "Test Image",
        "description": "This is a test image description."
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                resp_body = response.read().decode('utf-8')
                resp_data = json.loads(resp_body)
                print("Success! Response:", json.dumps(resp_data, indent=2))
                if "_id" in resp_data and resp_data["filename"] == payload["filename"]:
                    print("Verification Passed: Data matches and ID returned.")
                else:
                    print("Verification Failed: Response data mismatch.")
            else:
                print(f"Failed with status {response.status}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify()
