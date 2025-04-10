import json
from google.genai import types
import re
from llm_configs.gemini_config import gemini_client_setup

gemini_client = gemini_client_setup()
def validate_generated_code_gemini(message:dict):
    try:
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=json.dumps(message)),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=[
                types.Part.from_text(text="""
                    You are a senior developer reviewing a modular p5.js game based on the user's prompt.
                     Responsibilities:
                    - Check if the game logic is complete, valid, and readable
                    - Fix small missing pieces (e.g., scoring, collisions, script order)
                    - DO NOT over-refactor. Keep changes minimal and beginner-friendly
                    - Return JSON with all files even if unchanged
                   
                    Final Output Format:
                    Return ONLY this JSON (no markdown):
                    {
                      "status": 200,
                      "files": {
                        "index.html": "<code>",
                        "sketch.js": "<code>",
                        ...
                      },
                      "ai_assistance_message": "full explanation of the code"
                    }
                """),
            ],
        )
        response = gemini_client.models.generate_content(
            model='gemini-2.5-pro-exp-03-25',
            contents=contents,
            config=generate_content_config,
        )
        raw_text = response.text
        if raw_text.startswith("```json"):
            raw_text = re.sub(r"^```json\s*", "", raw_text)
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

        try:
            parsed_data = json.loads(raw_text)
            return parsed_data
        except json.JSONDecodeError as e:
            print("[JSONDecodeError]", str(e))
            return {
                "status": 500,
                "ai_assistance_message": f"Failed to parse Gemini response: {str(e)}",
                "raw": raw_text
            }
    except Exception as e:
        print("Error refining prompt:", e)
        return {
            "status": 500,
            "ai_assistance_message": f"Error generating code with Claude: {str(e)}"
        }


def edit_generated_code_gemini(message: str):
    try:
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=json.dumps(message)),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=[
                types.Part.from_text(text="""
                    You are a senior developer reviewing and updating an existing modular p5.js game based on a user's follow-up prompt.
                    Responsibilities:
                    - Carefully read the user's instruction and the provided existing code files.
                    - Only modify parts of the code that are directly relevant to the user's instruction.
                    - Ensure game logic, script load order, and interactivity remain valid.
                    - Do not over-refactor. Keep your changes minimal, clear, and beginner-friendly.
                    - If a file doesn’t need changes, include it as-is.
                    - If something is missing to fulfill the instruction (like new variables or logic), add only what’s necessary.
                    
                    Input Format:
                    {
                      "prompt": "User wants the game to increase speed every 3 points instead of 5",
                      "files": {
                        "index.html": "<existing_code>",
                        "sketch.js": "<existing_code>",
                        ...
                      }
                    }
                    
                    Final Output Format:
                    Return ONLY this JSON (no markdown or explanation before/after):
                    {
                      "status": 200,
                      "files": {
                        "index.html": "<possibly updated code>",
                        "sketch.js": "<possibly updated code>",
                        ...
                      },
                      "ai_assistance_message": "Concise explanation of what was changed"
                    }
                """),
            ],
        )
        response = gemini_client.models.generate_content(
            model='gemini-2.5-pro-exp-03-25',
            contents=contents,
            config=generate_content_config,
        )
        raw_text = response.text
        if raw_text.startswith("```json"):
            raw_text = re.sub(r"^```json\s*", "", raw_text)
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

        try:
            parsed_data = json.loads(raw_text)
            return parsed_data
        except json.JSONDecodeError as e:
            print("[JSONDecodeError]", str(e))
            return {
                "status": 500,
                "ai_assistance_message": f"Failed to parse Gemini response: {str(e)}",
                "raw": raw_text
            }
    except Exception as e:
        print("Error refining prompt:", e)
        return {
            "status": 500,
            "ai_assistance_message": f"Error generating code with Claude: {str(e)}"
        }

