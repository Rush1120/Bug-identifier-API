from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

def get_model():
    """Get the configured Gemini model instance."""
    return model 