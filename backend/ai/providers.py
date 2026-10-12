from __future__ import annotations

import re
from typing import Dict, List


class IntentClassifier:
    """Simple local intent classifier for the starter project."""

    def __init__(self) -> None:
        self.intent_rules: Dict[str, List[str]] = {
            "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
            "time": ["time", "clock", "date"],
            "open": ["open", "launch", "start"],
            "search": ["search", "find", "lookup"],
            "weather": ["weather"],
        }

    def predict(self, text: str) -> str:
        lowered = re.sub(r"\s+", " ", text.lower()).strip()
        if not lowered:
            return "empty"

        for intent, keywords in self.intent_rules.items():
            if any(keyword in lowered for keyword in keywords):
                return intent
        return "default"
