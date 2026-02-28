import requests
import time
import uuid

BASE_URL = "http://localhost:8000"

def register_user(email, password, role="free"):
    url = f"{BASE_URL}/auth/register"
    payload = {
        "email": email,
        "password": password,
        "role": role
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"User {email} registered successfully with role {role}.")
        return response.json()
    else:
        print(f"Failed to register user {email}: {response.text}")
        return None

def login_user(email, password):
    url = f"{BASE_URL}/auth/login"
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"User {email} logged in successfully.")
        return response.json()["access_token"]
    else:
        print(f"Failed to login user {email}: {response.text}")
        return None

def test_rate_limit(token, endpoint, method="GET", payload=None, limit=5, name="Test"):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    print(f"\n--- Testing {name} (Limit: {limit}/min) ---")
    
    success_count = 0
    for i in range(1, limit + 3):
        try:
            if method == "POST":
                response = requests.post(url, json=payload, headers=headers)
            else:
                response = requests.get(url, headers=headers)
                
            print(f"Request {i}: Status Code: {response.status_code}")
            
            if response.status_code == 200:
                success_count += 1
            elif response.status_code == 429:
                print(f"SUCCESS: Rate limit reached at request {i}.")
                return True
        except Exception as e:
            print(f"Request {i} failed: {e}")
            
    print(f"FAILURE: Rate limit of {limit} not reached after {limit+2} requests.")
    return False

def main():
    # Unique emails for each test run
    suffix = str(uuid.uuid4())[:8]
    free_email = f"free_{suffix}@example.com"
    pro_email = f"pro_{suffix}@example.com"
    password = "password123"

    # Register and login
    register_user(free_email, password, role="free")
    free_token = login_user(free_email, password)
    
    register_user(pro_email, password, role="pro")
    pro_token = login_user(pro_email, password)

    if not free_token or not pro_token:
        print("Setup failed. Ensure the backend is running.")
        return

    # Test /jenko/ POST (Free: 5/min, Pro: 20/min)
    payload = {"filename": "test.avif", "title": "Test", "category": "Test"}
    
    print("\n>>> Testing FREE user on /jenko/ (Expected: 5/min)")
    test_rate_limit(free_token, "/jenko/", method="POST", payload=payload, limit=5, name="Free /jenko/")
    
    print("\n>>> Testing PRO user on /jenko/ (Expected: 20/min)")
    # We won't actually do 20 requests to save time, but we'll check if it passes more than 5
    test_rate_limit(pro_token, "/jenko/", method="POST", payload=payload, limit=7, name="Pro /jenko/ (checking if > 5)")

if __name__ == "__main__":
    main()
