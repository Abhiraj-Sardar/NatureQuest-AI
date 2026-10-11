import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import ollama
from ollama import ResponseError
from .config import OLLAMA_HOST, OLLAMA_MODEL, FRONTEND_ORIGIN
from .prompts import QUEST_SYSTEM, NATURALIST_SYSTEM
from .schemas import QuestRequest, AskRequest

app = FastAPI(title="NatureQuest AI API", version="1.0.0",
              description="Local-first outdoor quests and nature Q&A powered by Ollama.")
app.add_middleware(CORSMiddleware, allow_origins=[FRONTEND_ORIGIN, "http://127.0.0.1:5173"],
                   allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
client = ollama.Client(host=OLLAMA_HOST)

def model_reply(system: str, prompt: str) -> str:
    try:
        result = client.chat(model=OLLAMA_MODEL,
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
            options={"temperature":0.5})
        return result["message"]["content"].strip()
    except ResponseError as exc:
        if exc.status_code == 404:
            raise HTTPException(503, f"Model '{OLLAMA_MODEL}' not found. Run `ollama pull {OLLAMA_MODEL}` or update backend/.env.")
        raise HTTPException(502, f"Ollama model error: {exc}")
    except Exception as exc:
        raise HTTPException(503, f"Cannot connect to Ollama at {OLLAMA_HOST}. Start Ollama and check the model. Details: {exc}")

def parse_json(text: str):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].removesuffix("```").strip()
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("No JSON object in model response")
    return json.loads(text[start:end+1])

@app.get("/")
def root():
    return {"name":"NatureQuest AI", "health":"/health", "docs":"/docs"}

@app.get("/health")
def health():
    try:
        data = client.list()
        names = [m.model for m in data.models]
        available = any(n == OLLAMA_MODEL or n.startswith(OLLAMA_MODEL + ":") for n in names)
        return {"status":"ok", "ollama_connected":True, "model":OLLAMA_MODEL, "model_available":available}
    except Exception as exc:
        return {"status":"degraded", "ollama_connected":False, "model":OLLAMA_MODEL, "detail":str(exc)}

@app.post("/api/quest")
def create_quest(request: QuestRequest):
    prompt = (f"Create an outdoor quest lasting {request.duration_minutes} minutes. "
              f"Setting: {request.setting}. Difficulty: {request.difficulty}. "
              f"Interests: {request.interests or 'nature details'}.")
    raw = model_reply(QUEST_SYSTEM, prompt)
    try:
        quest = parse_json(raw)
        required = ["title","intro","steps","look_for","safety_tip","screen_free_tip"]
        if not all(k in quest for k in required) or not isinstance(quest["steps"], list) or not isinstance(quest["look_for"], list):
            raise ValueError("Missing fields or lists")
        return {"quest":quest, "model":OLLAMA_MODEL}
    except (ValueError, json.JSONDecodeError) as exc:
        raise HTTPException(502, f"Could not parse quest response; please retry. Details: {exc}")

@app.post("/api/ask")
def ask_naturalist(request: AskRequest):
    prompt = f"Question: {request.question}\n"
    if request.observation.strip():
        prompt += f"Observation (not verified identification): {request.observation.strip()}\n"
    prompt += "Answer in 2-5 short paragraphs."
    return {"answer":model_reply(NATURALIST_SYSTEM, prompt), "model":OLLAMA_MODEL}
