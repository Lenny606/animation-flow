from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from pathlib import Path
import io
from PIL import Image

# Load env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_MODEL_IMAGEN_KEY") or os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

model_id = "gemini-2.5-flash-image"
prompt = "A cute robot painter, digital art style"

print(f"Testing model: {model_id}")

try:
    print("Trying generate_content...")
    response = client.models.generate_content(
        model=model_id,
        contents=prompt
    )
    
    print(f"Response parts: {len(response.candidates[0].content.parts)}")
    for i, part in enumerate(response.candidates[0].content.parts):
        if part.inline_data:
            print(f"Part {i}: Inline data found (image!)")
            img = Image.open(io.BytesIO(part.inline_data.data))
            img.save("test_gemini_image.png")
            print("Image saved to test_gemini_image.png")
        elif part.text:
            print(f"Part {i}: Text - {part.text[:50]}...")
        else:
            print(f"Part {i}: Unknown type")

except Exception as e:
    print(f"generate_content failed: {e}")

try:
    print("\nTrying generate_images...")
    response = client.models.generate_images(
        model=model_id,
        prompt=prompt,
        config=types.GenerateImagesConfig(number_of_images=1)
    )
    print(f"Generated images: {len(response.generated_images)}")
    if response.generated_images:
        image_data = response.generated_images[0].image
        if isinstance(image_data, bytes):
            img = Image.open(io.BytesIO(image_data))
            img.save("test_gemini_image_method.png")
        else:
            image_data.save("test_gemini_image_method.png")
        print("Image saved to test_gemini_image_method.png")
except Exception as e:
    print(f"generate_images failed: {e}")
