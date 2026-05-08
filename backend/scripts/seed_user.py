import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
import bcrypt

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import get_settings

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

async def seed_user():
    print("Starting direct user seeder...")
    settings = get_settings()
    
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    collection = db["users"]
    
    # Test credentials
    email = "tomas@example.com"
    password = "Password123!"
    hashed_password = get_password_hash(password)
    
    # Check if user already exists
    existing_user = await collection.find_one({"email": email})
    
    if existing_user:
        print(f"User {email} already exists. Updating password...")
        await collection.update_one(
            {"_id": existing_user["_id"]},
            {"$set": {"hashed_password": hashed_password}}
        )
    else:
        print(f"Creating test user: {email}")
        user_in = {
            "email": email,
            "hashed_password": hashed_password,
            "role": "admin"
        }
        await collection.insert_one(user_in)
    
    print("\n-------------------")
    print("Test User Created!")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print("Role: admin")
    print("-------------------\n")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_user())
