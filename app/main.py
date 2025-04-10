from fastapi import FastAPI
import os
import socket
from dotenv import load_dotenv
from app.routes import generate_chat_route
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI(title='Playable GPT AI')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_chat_route.router, prefix='/generate',tags=["generate"])

hostname = socket.gethostname()
port = os.getenv("PORT", "8000")

@app.get('/')
def generate_chat_health():
    return {
        "status": 200,
        "message": "Backend is running",
        "hostname": hostname,
        "port": port
    }