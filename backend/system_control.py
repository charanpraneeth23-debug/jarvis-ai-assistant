from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


@dataclass
class Settings:
    assistant_name: str = "Jarvis"
    llm_provider: str = os.getenv("LLM_PROVIDER", "local")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "")
    wake_word_enabled: bool = os.getenv("WAKE_WORD_ENABLED", "false").lower() == "true"
    system_control_enabled: bool = os.getenv("SYSTEM_CONTROL_ENABLED", "true").lower() == "true"


settings = Settings()
