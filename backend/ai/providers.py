from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


class AIProvider:
    """Base class for AI providers."""

    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        raise NotImplementedError


class LocalProvider(AIProvider):
    """Local AI provider using rule-based responses."""

    def __init__(self, model_name: Optional[str] = None) -> None:
        self.model_name = model_name or "local-mini"

    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        return f"Local model response for: {prompt}"


class OpenAIProvider(AIProvider):
    """OpenAI ChatGPT API provider."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: str = "gpt-3.5-turbo") -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = (base_url or os.getenv("OPENAI_BASE_URL", "")).rstrip("/")
        self.model = model

        if not self.base_url:
            self.base_url = "https://api.openai.com/v1"

    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        if not self.api_key:
            return "Error: OpenAI API key not configured. Please set OPENAI_API_KEY in .env"

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        system_prompt = "You are Jarvis, a helpful AI assistant. Be concise and friendly."
        if context:
            system_prompt += f" Context: {context}"

        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]

        payload = {"model": self.model, "messages": messages, "max_tokens": 500, "temperature": 0.7}

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                return f"OpenAI API error: {response.status_code} - {response.text}"
        except Exception as exc:  # pragma: no cover
            return f"Error connecting to OpenAI: {exc}"


class AIProviderFactory:
    """Factory for creating AI provider instances."""

    @staticmethod
    def create(provider_name: Optional[str] = None, **kwargs: Any) -> AIProvider:
        provider = (provider_name or os.getenv("LLM_PROVIDER", "local")).lower()
        if provider == "openai":
            return OpenAIProvider(**kwargs)
        return LocalProvider()
