from typing import Optional
from fastapi import WebSocket
import time
import json


async def send_ws_chat_response(websocket: WebSocket, payload: dict):
    try:
        await websocket.send_text(json.dumps({'payload': payload, 'state': 'ai_assistance_message'}))
    except Exception as e:
        print(f"[WebSocket Error] Failed to send message: {e}")

async def send_ws_chat_thinking_response(websocket: WebSocket, payload:dict):
    try:
        await websocket.send_text(json.dumps({'payload':payload, 'state':'thinking'}))
    except Exception as e:
        print(f"[WebSocket Error] Failed to send message: {e}")

async def send_ws_files_response(websocket: WebSocket, files:dict):
    try:
        await websocket.send_text(json.dumps({'payload':files, 'state':'files_shared'}))
    except Exception as e:
        print(f"[WebSocket Error] Failed to send message: {e}")

def ai_assistance_payload(status:int,message:str,is_not_related_to_game:Optional[str] = None ):
    payload = {
        "status": status,
        "role": "ai_assistance",
        "message": message,
        "time_stamp": int(time.time() * 1000)
    }

    if is_not_related_to_game is not None:
        payload["is_not_related_to_game"] = is_not_related_to_game

    return payload

