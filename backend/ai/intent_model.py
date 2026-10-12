"""AI-related modules for intent detection and provider integration."""

from backend.ai.intent_model import IntentClassifier
from backend.ai.providers import AIProviderFactory

__all__ = ["IntentClassifier", "AIProviderFactory"]
