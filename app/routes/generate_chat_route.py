from fastapi import APIRouter
from pydantic import BaseModel
from starlette.websockets import WebSocket
import json
import asyncio

from utils.chat_history_utils import save_chat, SaveChatArgs, SaveFileArgs, save_files
from utils.generate_code_util import generate_code_claude
from utils.handle_exception import handle_exception
from utils.response import send_ws_chat_response, ai_assistance_payload, send_ws_chat_thinking_response, \
    send_ws_files_response
from utils.validate_generated_code import validate_generated_code_gemini, edit_generated_code_gemini
from utils.validate_prompt import validate_user_prompt, refined_prompt_for_claude

router = APIRouter()

@router.get('/health')
def generate_chat_health():
 return {
         "status": 200,
         "message": "generate chat api working",
        }

@router.websocket('/ws/chat')
async def generate_websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            chat = json.loads(data)

            validated_prompt = json.loads(validate_user_prompt(chat['message']))
            print('\n validate_prompt->',validated_prompt)
            await send_ws_chat_thinking_response(websocket, ai_assistance_payload(200,validated_prompt['ai_assistance_message']))
            # # for testing purpose
            # await asyncio.sleep(3)
            # await send_ws_chat_thinking_response(websocket, ai_assistance_payload(200,validated_prompt['ai_assistance_message']))
            # await asyncio.sleep(3)
            # await send_ws_chat_thinking_response(websocket,
            #                                      ai_assistance_payload(200, validated_prompt['ai_assistance_message']))
            # await asyncio.sleep(3)
            # await send_ws_chat_response(websocket,
            #                                      ai_assistance_payload(200, validated_prompt['ai_assistance_message']))


            if validated_prompt['status'] == 200:
                save_chat(SaveChatArgs(user_id=chat['user_id'], role='user' ,message=validated_prompt['message']))
                save_files(SaveFileArgs(user_id=chat['user_id'],
                                        files=json.dumps(validated_prompt['message'])))
                claude_prompt_refined = json.loads(refined_prompt_for_claude(validated_prompt['message']))
                print('\n claude_prompt_refined->', claude_prompt_refined)
                await send_ws_chat_thinking_response(websocket, ai_assistance_payload(200, claude_prompt_refined['ai_assistance_message']))

                claude_code_generated = json.loads(generate_code_claude(claude_prompt_refined['message']))
                print('\n claude_code_generated->', claude_code_generated)
                await send_ws_chat_thinking_response(websocket, ai_assistance_payload(200, claude_code_generated['ai_assistance_message']))
                gemini_validate_code = validate_generated_code_gemini(claude_code_generated)
                print('\n gemini_validate_code->', gemini_validate_code)
                if gemini_validate_code['status'] == 200:
                    #[TODO] will add save chat once we write the RAG and context provider logic
                    # save_chat(SaveChatArgs(user_id=chat['user_id'], role='ai_assistance', message=gemini_validate_code['ai_assistance_message']))
                    await send_ws_chat_response(websocket, ai_assistance_payload(200, gemini_validate_code['ai_assistance_message']))
                    await send_ws_files_response(websocket,gemini_validate_code['files'])
                else:
                    #[TODO] will add save chat once we write the RAG and context provider logic
                    # save_chat(SaveChatArgs(user_id=chat['user_id'], role='ai_assistance',
                    #                        message=claude_code_generated['ai_assistance_message']))
                    await send_ws_chat_response(websocket, ai_assistance_payload(200, claude_code_generated['ai_assistance_message']))
                    #[TODO] will add save chat once we write the RAG and context provider logic
                    # save_files(SaveFileArgs(user_id=chat['user_id'],
                    #                        files=json.dumps(claude_code_generated['files'])))
                    await send_ws_files_response(websocket, claude_code_generated['files'])
            else:
                #[TODO] will add save chat once we write the RAG and context provider logic
                # save_chat(SaveChatArgs(user_id=chat['user_id'], role='ai_assistance',
                #                        message=validated_prompt['ai_assistance_message']))
                print('\n else_block_validate_code->', validated_prompt)
                await send_ws_chat_response(websocket, ai_assistance_payload(400,validated_prompt['ai_assistance_message']))



    except Exception as e:
        return handle_exception(e, "Failed to process.")

@router.websocket('/ws/chat/edit')
async def generate_websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print("edit triggered",data)
            gemini_edited_code = edit_generated_code_gemini(data)
            await send_ws_chat_response(websocket,
                                        ai_assistance_payload(400, gemini_edited_code['ai_assistance_message']))
            #[TODO] will add save chat once we write the RAG and context provider logic
            # save_chat(SaveChatArgs(user_id=chat['user_id'], role='ai_assistance',
            #                        message=gemini_edited_code['ai_assistance_message']))
            await send_ws_files_response(websocket, gemini_edited_code['files'])
            #[TODO] will add save chat once we write the RAG and context provider logic
            # save_files(SaveFileArgs(user_id=chat['user_id'],
            #                        files=json.dumps(gemini_edited_code['files'])))

            print('\n gemini_edited_code->', gemini_edited_code)

    except Exception as e:
        return handle_exception(e, "Failed to process.")



