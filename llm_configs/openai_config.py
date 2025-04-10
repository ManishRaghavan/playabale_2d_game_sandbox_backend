import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
def openai_client_setup():
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return openai_client