# EcoQuest — Environmental Sustainability App for Teens (Python / FastAPI)



This is the FastAPI powered Backend that fuels EcoQuest's AI Features such as EcoEcho(RAG based sustainability chatbot), litterLens(Computer Vision powered Trash Detector), and AI powered dynamic sustainability quizzes. The codebase encompasses of modular services, coherent dependency management, and clear API endpoints that integrates Google Gemini, Google Custom Search, and Computer Vision techniques. 



## Quick Snapshot
- Technical Stack: Python, FastAPI, LangChain, Google Generative AI (Gemini) API, Google Custom Search.
- Purpose: Answer sustainability questions with context, detect/advise on trash from images, and emit multi-choice quiz content. Respond to sustainability based questions with Realtime data as context, classify trash and give disposal suggestions, and provide multiple choice question based Environmental Quiz. 
- Install Dependencies : 'pip install -r requirements.txt'
- Run locally: `uvicorn main:app --reload'

---

## Why this structure?
The project follows the best practice of separation of concerns into several services so each module can be developed and test independently thereby implementing loose coupling. This makes it easier to debug the code, and iterate on it for further enhancements. 

---

## Core components
- Entry point: [main.py](main.py)
- API router & auth: [`app.api.endpoints.get_current_user`](app/api/endpoints.py) and the routes in [app/api/endpoints.py](app/api/endpoints.py)
- LangChain / Gemini integration: [`app.services.langchain_service.sustainability_chatbot_response`](app/services/langchain_service.py)
- Google Custom Search -> Doc context: [`app.services.gcs_service.search_google`](app/services/gcs_service.py)
- Trash detection and Roboflow hooks: [`app.services.trash_detection.classify_and_advise`](app/services/trash_detection.py) plus helpers [`identify_object`](app/services/trash_detection.py) and [`trash_detection`](app/services/trash_detection.py)
- Quiz generator using Gemini: [`app.services.quiz_bot.quiz_bot_response`](app/services/quiz_bot.py)
- Request/response schemas: [`app.models.schemas.QueryRequest`](app/models/schemas.py), [`app.models.schemas.GeminiResponse`](app/models/schemas.py)

---

## Endpoints (high-level)
- GET `/test` — sanity test that returns a lightweight json response to check the health of the server.
- POST `/ask` — accepts a question through the Chat interface and returns a LLM-backed answer. Uses Google Custom Search to build contextual documents and `sustainability_chatbot_response` to generate responses
- POST `/classify-trash` — multipart image upload, returns structured analysis (aims to parse JSON from Gemini output). - POST `/quiz-bot` — returns an environmental quiz generate dynamically by LLM.

See routes and authentication logic in [app/api/endpoints.py](app/api/endpoints.py).

---

## Environment & secrets
The app reads env vars from `.env.local` (example file included). Key variables:
- GEMINI_API_KEY — Gemini / Google Generative API key
- GOOGLE_API_KEY, GCS_SEARCH_ENGINE_ID — for Google Custom Search
- SUPABASE_JWT_SECRET — used to validate incoming Bearer tokens

File: [.env.local](.env.local)

Security note: Never commit real credentials to version control. This repo's `.gitignore` already excludes `.env` files.

---

## Local setup (one-liner)
1. Create a venv and install deps:
```bash
python -m venv .venv
.venv/Scripts/activate   # or `source .venv/bin/activate` on macOS/Linux
pip install -r [requirements.txt](http://_vscodecontentref_/0)
2. Run program
uvicorn main:app --reload
