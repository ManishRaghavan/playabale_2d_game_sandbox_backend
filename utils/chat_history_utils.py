from llm_configs.superbase_client import  supabase_client_setup
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

supabase_client = supabase_client_setup()
class SaveChatArgs(BaseModel):
    user_id: str
    role: str
    message: str

def save_chat(args: SaveChatArgs):
    try:

        response = supabase_client.table("chat_context").insert({
            "user_id": args.user_id,
            "role": args.role,
            "message": args.message
        }).execute()

        print('chat_saved ->', response)
        if response.data:
            return True
        else:
            return {
                "status": False,
                "error": "No data returned from Supabase"
            }

    except Exception as e:
        print(f"Error saving chat message: {e}")
        return {
            "status": False,
            "error": f"Failed to save chat message: {str(e)}"
        }


class SaveFileArgs(BaseModel):
    user_id: str
    files: str

def save_files(args: SaveFileArgs):
    try:
        response = supabase_client.table("files_stored").insert({
            "user_id": args.user_id,
            "files": args.files
        }).execute()

        print('files_saved ->', response)
        if response.data:
            return True
        else:
            return {
                "status": False,
                "error": "No data returned from Supabase"
            }

    except Exception as e:
        print(f"Error saving chat message: {e}")
        return {
            "status": False,
            "error": f"Failed to save chat message: {str(e)}"
        }
