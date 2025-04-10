from llm_configs.openai_config import openai_client_setup

openai_client = openai_client_setup()

def validate_user_prompt(message:str):
    message = [{
                    "role": "system",
                    "content": """You are an assistant that refines user prompts to make them more clear, actionable, 
                        and suitable for a coding assistant. Don't add unnecessary information or make the AI 
                        overdo things. Just clarify the existing request. Always check if the user prompt is 2d game related.  
        
                        If prompt is game-related:
                        {
                          "status": 200,
                          "message": "<clarified prompt>",
                          "ai_assistance_message":"<explain what you have done to the user>"
                           "is_not_related_to_game": "false" or "true"
                        }
                        
                        If not game-related:
                        {
                          "status": 404,
                          "ai_assistance_message": "Hey there! 😊 I'm excited to help — but could you please ask something related to a 2D game you'd like to build?"
                          "is_not_related_to_game": "false" or "true"
                        }
                    """
                },
                {
                    "role": "user",
                    "content": f"Refine this user prompt for a coding task: {message}"
                }]
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=message,
            temperature=0.2,
            max_tokens=2000
        )
        refined = response.choices[0].message.content.strip()
        return refined

    except Exception as e:
        print("Error refining prompt:", e)
        return message


def refined_prompt_for_claude(message:str):
    message = [
                {
                    "role": "system",
                    "content": """
            You are an assistant that turns simple 2D game ideas into detailed technical game specifications in **Markdown format**.
            
            Your goal is to expand the user's refined prompt into a clear, concise document that includes:
            
            ---
            
            ## Markdown Format Output (No JSON, no explanation outside Markdown):
            
            ##Game Title: [A short descriptive title]
            
            ###Game Description:
            Briefly describe the core objective of the game, based on the user’s idea.
            
            ###Game Mechanics:
            - Bullet list of all key mechanics (player movement, enemy behavior, win/loss conditions, scoring).
            - Mention if it’s level-based, endless, or timed.
            
            ###Controls:
            - Keyboard controls (e.g., left/right arrows, spacebar)
            - Mouse or touch if mentioned
            
            ###File Structure:
            List and describe each file needed. Use this default if not specified:
            - `index.html`: loads scripts + canvas
            - `sketch.js`: setup(), draw(), preload()
            - `player.js`: player movement and control
            - `game.js`: game state, scoring, object spawning
            
            ###Assets:
            - Mention any image/sound URLs provided by the user
            - Otherwise, say “use p5.js shapes (rect, ellipse, etc.)”
            
            ###Implementation Guidelines:
            - Must be simple and modular
            - Use only p5.js and optionally master.js
            - Use plain JavaScript (no ES6 classes unless needed)
            - Add short comments to guide the code
            
            Only return the **Markdown file** like a message, nothing else.
            Your final response format must be:
            {
              "status": 200,
              "message": "<the full markdown specification>"
              "ai_assistance_message":"<explain what you have done here to the user>"
            }
            """
    },
        {
            "role": "user",
            "content": f"""Create a game specification in markdown for the following refined game idea:{message}"""
        }
]

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=message,
            temperature=0.2,
            max_tokens=3000
        )
        refined = response.choices[0].message.content.strip()
        return refined

    except Exception as e:
        print("Error refining prompt:", e)
        return {
            "status": 500,
            "ai_assistance_message": f"Error generating code with Claude: {str(e)}"
        }
