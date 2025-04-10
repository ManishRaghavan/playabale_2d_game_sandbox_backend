import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
def claude_client_setup():
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    claude_client = anthropic.Anthropic(api_key=claude_api_key)
    return claude_client