# NatureQuest AI 🌿
A local-first outdoor discovery companion powered by an open-weight model through Ollama.

## What it does
- Generates safe outdoor quests based on duration, setting, difficulty, and interests.
- Answers nature questions using a local Qwen model.
- Stores your field journal and quest progress in browser localStorage.
- Sends prompts to your own Ollama service, not a hosted AI API.
- Runs without internet after you install dependencies and download the model.

## Stack
React + Vite · FastAPI · Ollama · Qwen open-weight model · browser localStorage

## 1. Install Ollama and the model
Install Ollama from https://ollama.com/download, then:
```bash
ollama pull qwen2.5:3b
ollama run qwen2.5:3b
```
If this tag is unavailable, choose an available Qwen text model and update `OLLAMA_MODEL` in `backend/.env`. Smaller models are more practical on modest laptops.

## 2. Run the backend
```bash
cd backend
python -m venv .venv
```
Windows PowerShell: `.venv\Scripts\Activate.ps1`
macOS/Linux: `source .venv/bin/activate`
```bash
pip install -r requirements.txt
```
Copy `.env.example` to `.env`, then:
```bash
uvicorn app.main:app --reload --port 8000
```
Check http://localhost:8000/health and http://localhost:8000/docs.

## 3. Run the frontend
In a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173.

## 4. Try it
1. Generate a 15- or 20-minute quest.
2. Read the instructions, then put your phone away while exploring.
3. Mark completed steps and write an observation in Field Journal.
4. Ask the local naturalist a question.

## Project structure
```text
naturequest-ai/
├── README.md
├── .gitignore
├── backend/
│   ├── .env.example
│   ├── requirements.txt
│   └── app/{__init__.py,config.py,schemas.py,prompts.py,main.py}
└── frontend/
    ├── package.json
    ├── index.html
    ├── vite.config.js
    └── src/{main.jsx,api.js,App.jsx,styles.css}
```

## Privacy and safety
Journal data stays in browser localStorage. AI questions go to Ollama running on your computer. Download model weights before going offline. Do not eat or touch wild plants or mushrooms based on AI answers; keep a safe distance from wildlife, stay on permitted paths, and treat model output as educational rather than authoritative. This MVP does not verify species identity or use GPS.

## Troubleshooting
- Ollama connection issue: start Ollama and run `ollama list`.
- Model missing: `ollama pull qwen2.5:3b` or update `.env` to match `ollama list`.
- Backend error: activate the virtual environment and install `requirements.txt`.
- Frontend API error: ensure backend port 8000 is running.
- Slow output: use a smaller model and close memory-heavy applications.

## Why open innovation matters
A downloadable open-weight model makes local inference possible: personal observations need not go to a third-party AI API, there is no per-request cloud AI bill, and the model can be swapped or the prompts adapted. NatureQuest uses AI to plan the outing; the screen should be the shortest part of the experience.

## Future upgrades
Local vision model for photo-based observations, exportable journal, seasonal quest packs, installable PWA, SQLite option, and multilingual support.
