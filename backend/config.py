from __future__ import annotations

import datetime
import random
from dataclasses import dataclass, field
from typing import Any, Dict, List

from backend.config import settings
from backend.system_controller import SystemController
from backend.voice_manager import VoiceManager


@dataclass
class AssistantResponse:
    success: bool
    message: str
    action: str = "reply"
    metadata: Dict[str, Any] = field(default_factory=dict)


class JarvisAssistant:
    def __init__(self) -> None:
        self.system = SystemController()
        self.voice = VoiceManager()
        self.name = settings.assistant_name
        self.intent_handlers = {
            "greeting": self._handle_greeting,
            "time": self._handle_time,
            "open": self._handle_open,
            "search": self._handle_search,
            "weather": self._handle_weather,
            "default": self._handle_default,
        }

    def process_text(self, text: str) -> AssistantResponse:
        user_input = (text or "").strip()
        if not user_input:
            return AssistantResponse(False, "Please provide a command.", "empty")

        intent = self._detect_intent(user_input)
        return self.intent_handlers.get(intent, self.intent_handlers["default"])(user_input)

    def _detect_intent(self, text: str) -> str:
        lower = text.lower()

        if any(keyword in lower for keyword in ["hello", "hi", "hey", "good morning", "good evening"]):
            return "greeting"
        if any(keyword in lower for keyword in ["time", "clock", "date"]):
            return "time"
        if any(keyword in lower for keyword in ["open", "launch", "start"]):
            return "open"
        if any(keyword in lower for keyword in ["search", "find", "lookup"]):
            return "search"
        if "weather" in lower:
            return "weather"
        return "default"

    def _handle_greeting(self, text: str) -> AssistantResponse:
        greeting_options = [
            "Hello! I am Jarvis, ready to help.",
            "Hi there. How can I assist you today?",
            "Good day. I am online and ready for your requests.",
        ]
        return AssistantResponse(True, random.choice(greeting_options), "greeting")

    def _handle_time(self, text: str) -> AssistantResponse:
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        current_date = now.strftime("%A, %d %B %Y")
        return AssistantResponse(
            True,
            f"The current time is {current_time}. Today is {current_date}.",
            "time",
            {"time": current_time, "date": current_date},
        )

    def _handle_open(self, text: str) -> AssistantResponse:
        target = text.replace("open", "", 1).strip()
        if not target:
            return AssistantResponse(False, "What would you like me to open?", "open")

        result = self.system.open_application(target)
        if result.get("success"):
            return AssistantResponse(True, f"Opening {target}.", "open", {"target": target})
        return AssistantResponse(False, f"I couldn't open {target}: {result.get('error', 'Unknown error')}", "open")

    def _handle_search(self, text: str) -> AssistantResponse:
        query = text.replace("search", "", 1).replace("find", "", 1).replace("lookup", "", 1).strip()
        if not query:
            return AssistantResponse(False, "What should I search for?", "search")
        return AssistantResponse(True, f"Searching for '{query}' using your configured search backend.", "search", {"query": query})

    def _handle_weather(self, text: str) -> AssistantResponse:
        return AssistantResponse(True, "Weather support is ready to be connected to an API or data source.", "weather")

    def _handle_default(self, text: str) -> AssistantResponse:
        return AssistantResponse(
            True,
            "I heard you. I can help with system control, voice commands, and AI tasks.",
            "reply",
            {"input": text},
        )

    def process_command(self, command: str) -> Dict[str, Any]:
        result = self.process_text(command)
        return {
            "success": result.success,
            "message": result.message,
            "action": result.action,
            "metadata": result.metadata,
        }


def run_cli() -> None:
    assistant = JarvisAssistant()
    print(f"{settings.assistant_name} is ready. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("Jarvis offline.")
            break
        response = assistant.process_command(user_input)
        print(f"Jarvis: {response['message']}")


if __name__ == "__main__":
    run_cli()
