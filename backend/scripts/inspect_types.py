from google.genai import types
print(f"genai.types attributes: {[a for a in dir(types) if 'Image' in a or 'Config' in a]}")
