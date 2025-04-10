from llm_configs.claude_config import claude_client_setup

claude_client = claude_client_setup()
def generate_code_claude(message:str):
    print('generate code claude started',message)
    claude_system_prompt = """
    Your goal is to:
    - Understand the gameplay and mechanics from the user's prompt
    - Generate the complete HTML and modular JavaScript files
    - Ensure all logic is split into appropriate files for reusability and clarity
    
     Required Output Format (JSON only):
    {
      "status": 200,
      "files": {
        "index.html": "<html code>",
        "sketch.js": "// main loop code",
        "utils.js": "// helper functions",
        "player.js": "// player control",
        "enemy.js": "// enemy logic (if needed)",
        "obstacles.js": "// for objects or platforms",
        ...
      },
      "ai_assistance_message": "A short 5–7 line explanation of the game’s mechanics and implementation."
    }
    
     File Structure Instructions:
    - Always include `index.html` and `sketch.js`
    - For other files, dynamically decide based on game mechanics:
        - If there's a controllable character: create `player.js`
        - If there are enemies or falling objects: create `enemy.js` or `asteroid.js`
        - If there's shooting: include `bullet.js`
        - If there are collectibles/platforms: add `platform.js`, `obstacles.js`, etc.
        - Common logic like scoring/collisions: move to `game.js` or `engine.js`
    
     Guidelines:
    - Use plain JavaScript (no ES6 classes unless needed)
    - Use only p5.js or master.js — no external libraries
    - Comment each file appropriately
    - Keep files modular, even if short
    
     Only return the JSON object as output. No markdown, no explanations.
        {
      "status": 200,
      "files": {
        "index.html": "<html code here>",
        "sketch.js": "// JS code here",
        "utils.js": "// helper functions",
        ...
      },
      "ai_assistance_message": "Brief explanation of the game created, files created, its mechanics, and how it matches the prompt."
    }
    """

    try:
        response = claude_client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=10000,
            temperature=0.4,
            system=claude_system_prompt,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        content = response.content[0].text.strip()
        return content

    except Exception as e:
        return {
            "status": 500,
            "ai_assistance_message": f"Error generating code with Claude: {str(e)}"
        }
