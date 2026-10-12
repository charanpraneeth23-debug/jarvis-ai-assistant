from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI
from pydantic import BaseModel

from backend.assistant import JarvisAssistant

app = FastAPI(title="Jarvis API", version="0.1.0")
assistant = JarvisAssistant()


class CommandRequest(BaseModel):
    text: str


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "assistant": "Jarvis"}


@app.post("/command")
def command(request: CommandRequest) -> Dict[str, Any]:
    return assistant.process_command(request.text)


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "Jarvis backend is running."}
