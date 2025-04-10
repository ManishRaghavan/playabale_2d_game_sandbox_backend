# Playable GPT Backend 🎮🤖

This is a FastAPI WebSocket-based backend built for an AI-powered 2D Game Development Platform.  
It supports real-time code generation, game file management, and AI-assisted game development workflows.

---

## Tech Stack

- Python 3.11
- FastAPI
- WebSocket Support
- Supabase (for Realtime DB & Chat)
- Multi-LLM Support (Claude, Gemini, OpenAI)
- Modular & Scalable Code Structure

---

## Project Structure

```
app/

🔹 routes/                  # API & WebSocket Routes
🔹 generate_chat_route.py

🔹 llm_configs/             # Configurations for Claude, Gemini, OpenAI, Supabase

🔹 utils/                   # Utility functions for chat history, code generation, validation

🔹 main.py                  # FastAPI App Entry Point

.env                         # Environment Variables
requirements.txt             # Python Dependencies
```

---

## Run Locally

Clone the project:

```bash
git clone https://github.com/your-username/playable_gpt_backend.git
cd playable_gpt_backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Deployment on Render.com

> Simple steps to deploy your FastAPI backend with WebSocket on Render:

1. Go to https://render.com/
2. Create New Web Service
3. Connect your GitHub repository
4. Set Build Command:
```bash
pip install -r requirements.txt
```
5. Set Start Command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
6. Add Environment Variables from your `.env` file in Render Dashboard
7. Click Deploy 🚀

---

## Environment Variables

Ensure to configure these variables:

```
SUPABASE_URL=
SUPABASE_API_KEY=
CLAUDE_API_KEY=
GEMINI_API_KEY=
OPENAI_API_KEY=
```

---

## API Endpoints

| Method | Endpoint                | Description                        |
|--------|-------------------------|-----------------------------------|
| WS     | /generate-chat          | WebSocket for AI Chat & Code Gen  |

---

## Features

- Real-time WebSocket-based chat
- Code generation using LLMs
- Chat history management
- Validate generated code
- Modular utils for handling exceptions, responses, prompts
- Easy to extend & customize

---

## License

MIT License © 2025 Manish RR

---

> Made with ❤️ for AI-powered Game Development.

