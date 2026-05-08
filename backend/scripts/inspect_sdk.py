from google import genai
import os
from dotenv import load_dotenv
from pathlib import Path

# Load env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

print(f"Client.models attributes: {dir(client.models)}")
