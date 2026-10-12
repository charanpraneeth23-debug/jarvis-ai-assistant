from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from backend.assistant import JarvisAssistant

app = FastAPI(title="Jarvis API", version="0.1.0")
assistant_local = JarvisAssistant(ai_provider="local")
assistant_ai = JarvisAssistant(ai_provider="openai")


class CommandRequest(BaseModel):
    text: str
    ai_mode: bool = False


class SpeakRequest(BaseModel):
    text: str


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "assistant": "Jarvis", "version": "0.1.0"}


@app.post("/command")
def command(request: CommandRequest) -> Dict[str, Any]:
    assistant = assistant_ai if request.ai_mode else assistant_local
    return assistant.process_command(request.text)


@app.post("/voice")
def voice() -> Dict[str, Any]:
    result = assistant_local.listen_and_respond()
    if result:
        return {"success": True, "text": "(voice input would be here)", "response": result.get("message", "No response")}
    return {"success": False, "message": "Voice not available or no speech detected"}


@app.post("/speak")
def speak(request: SpeakRequest) -> Dict[str, Any]:
    success = assistant_local.speak_response(request.text)
    return {"success": success, "message": "Response spoken" if success else "TTS not available"}


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "Jarvis backend is running. Use /docs for API documentation."}
