import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
def gemini_client_setup():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    gemini_client = genai.Client(api_key=gemini_api_key)
    return gemini_client
