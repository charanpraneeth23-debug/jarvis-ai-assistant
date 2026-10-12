from __future__ import annotations

import os
from typing import Any, Dict, Optional


class LocalProvider:
    def __init__(self, model_name: Optional[str] = None) -> None:
        self.model_name = model_name or "local-mini"

    def generate(self, prompt: str) -> str:
        return f"Local model response for: {prompt}"


class OpenAICompatibleProvider:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "")

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not configured.")
        return f"Cloud model response for: {prompt}"


class AIProviderFactory:
    @staticmethod
    def create(provider_name: Optional[str] = None) -> Any:
        provider = (provider_name or os.getenv("LLM_PROVIDER", "local")).lower()
        if provider == "openai":
            return OpenAICompatibleProvider()
        return LocalProvider()
