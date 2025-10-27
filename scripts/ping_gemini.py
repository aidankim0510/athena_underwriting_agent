# scripts/ping_gemini.py
import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

key = os.getenv("GEMINI_API_KEY")
assert key, "GEMINI_API_KEY missing in environment (.env)"
genai.configure(api_key=key)

print("== Available models supporting generateContent ==")
for m in genai.list_models():
    methods = getattr(m, "supported_generation_methods", []) or []
    if "generateContent" in methods:
        print("-", m.name)  # <-- copy one of these into GEMINI_MODEL

model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest")
print("\nTrying model:", model_name)
model = genai.GenerativeModel(model_name)
resp = model.generate_content("Return exactly the string: OK")
print("Response:", (resp.text or "").strip())