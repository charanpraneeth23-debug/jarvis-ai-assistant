from __future__ import annotations

import datetime
import random
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from backend.ai.providers import AIProviderFactory
from backend.config import settings
from backend.search_engine import SearchEngine
from backend.system_controller import SystemController
from backend.voice_manager import VoiceManager


@dataclass
class AssistantResponse:
    success: bool
    message: str
    action: str = "reply"
    metadata: Dict[str, Any] = field(default_factory=dict)


class JarvisAssistant:
    def __init__(self, ai_provider: Optional[str] = None) -> None:
        self.system = SystemController()
        self.voice = VoiceManager()
        self.search = SearchEngine()
        self.ai_provider = AIProviderFactory.create(ai_provider or settings.llm_provider)
        self.name = settings.assistant_name
        self.ai_mode = (ai_provider or settings.llm_provider).lower() == "openai"
        self.conversation_history: list[str] = []

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

        self.conversation_history.append(f"User: {user_input}")

        intent = self._detect_intent(user_input)
        handler_result = self.intent_handlers.get(intent, self.intent_handlers["default"])(user_input)

        if self.ai_mode and intent == "default":
            ai_response = self.ai_provider.generate(user_input, context=" ".join(self.conversation_history[-5:]))
            self.conversation_history.append(f"Jarvis: {ai_response}")
            return AssistantResponse(True, ai_response, "ai_reply", {"input": user_input})

        self.conversation_history.append(f"Jarvis: {handler_result.message}")
        return handler_result

    def _detect_intent(self, text: str) -> str:
        lower = text.lower()

        if any(keyword in lower for keyword in ["hello", "hi", "hey", "good morning", "good evening"]):
            return "greeting"
        if any(keyword in lower for keyword in ["time", "clock", "date"]):
            return "time"
        if any(keyword in lower for keyword in ["open", "launch", "start"]):
            return "open"
        if any(keyword in lower for keyword in ["search", "find", "lookup", "google", "wikipedia"]):
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
        query = text.replace("search", "", 1).replace("find", "", 1).replace("lookup", "", 1).replace("google", "", 1).replace("wikipedia", "", 1).strip()
        if not query:
            return AssistantResponse(False, "What should I search for?", "search")

        search_result = self.search.search(query)
        if search_result.get("success") and search_result.get("results"):
            results = search_result.get("results", [])
            message = f"Found {len(results)} results for '{query}':\n"
            for idx, res in enumerate(results[:3], 1):
                message += f"{idx}. {res.get('title', 'No title')}\n   {res.get('url', 'No URL')}\n"
            return AssistantResponse(True, message.strip(), "search", {"query": query, "results": results})
        else:
            return AssistantResponse(True, f"Searching for '{query}'. {search_result.get('message', '')}", "search", {"query": query})

    def _handle_weather(self, text: str) -> AssistantResponse:
        return AssistantResponse(True, "Weather support is ready to be connected to an API or data source.", "weather")

    def _handle_default(self, text: str) -> AssistantResponse:
        if self.ai_mode:
            ai_response = self.ai_provider.generate(text)
            return AssistantResponse(True, ai_response, "ai_reply", {"input": text})
        return AssistantResponse(
            True,
            "I heard you. I can help with system control, voice commands, searches, and AI tasks.",
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

    def listen_and_respond(self) -> Optional[Dict[str, Any]]:
        """Listen for voice input and process it."""
        if not self.voice.is_available():
            return None
        text = self.voice.listen_once()
        if text:
            return self.process_command(text)
        return None

    def speak_response(self, message: str) -> bool:
        """Speak the response message."""
        return self.voice.speak(message)


def run_cli() -> None:
    import sys

    ai_mode = "--ai" in sys.argv
    assistant = JarvisAssistant(ai_provider="openai" if ai_mode else "local")
    mode_name = "AI Mode (ChatGPT)" if ai_mode else "Local Mode"
    print(f"{assistant.name} is ready in {mode_name}. Type 'exit' to quit.")
    print("Commands: 'hello', 'time', 'search <query>', 'open <app>', or ask anything.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("Jarvis offline.")
            break
        response = assistant.process_command(user_input)
        print(f"Jarvis: {response['message']}")


if __name__ == "__main__":
    run_cli()
