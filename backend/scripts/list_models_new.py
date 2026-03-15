from google import genai
import os
from dotenv import load_dotenv
from pathlib import Path

# Load env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

print("Listing models with new SDK...")
for m in client.models.list():
    print(f"Name: {m.name}, Name (base): {m.base_model_id if hasattr(m, 'base_model_id') else 'N/A'}")
