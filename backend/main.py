from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from debate_engine import run_debate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class DebateRequest(BaseModel):
    decision: str
    rounds: int = 3


@app.post("/debate")
def debate(req: DebateRequest):
    return run_debate(req.decision, req.rounds)


@app.get("/health")
def health():
    return {"status": "ok"}