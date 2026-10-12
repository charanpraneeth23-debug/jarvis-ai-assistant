from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from backend.config import settings


@dataclass
class CommandResult:
    success: bool
    message: str
    data: Dict = field(default_factory=dict)


class JarvisAssistant:
    def __init__(self):
        self.name = settings.assistant_name
        self.modes = ["voice", "text", "system"]

    def process_text(self, text: str) -> CommandResult:
        user_input = (text or "").strip()
        if not user_input:
            return CommandResult(False, "No command provided.")

        lowered = user_input.lower()

        if "hello" in lowered or "hi" in lowered:
            return CommandResult(True, "Hello! I am Jarvis. How can I help you today?")

        if "time" in lowered:
            import datetime
            current = datetime.datetime.now().strftime("%H:%M:%S")
            return CommandResult(True, "The current time is " + current, {"time": current})

        if "open" in lowered:
            return CommandResult(True, f"I can open '{user_input}' in your desktop environment.", {"action": "open_app", "target": user_input})

        if "search" in lowered:
            return CommandResult(True, f"I can search for '{user_input}' using your configured search backend.", {"action": "search", "target": user_input})

        if "weather" in lowered:
            return CommandResult(True, "Weather support can be connected to a weather API provider.", {"action": "weather"})

        return CommandResult(True, "I heard you. I can help with system control, research, and voice commands.", {"action": "reply"})

    def process_command(self, command: str) -> Dict:
        result = self.process_text(command)
        return {
            "success": result.success,
            "message": result.message,
            "data": result.data,
        }


def run_cli() -> None:
    assistant = JarvisAssistant()
    print(f"{settings.assistant_name} is ready. Type 'exit' to quit.")
    while True:
        text = input("You: ")
        if text.strip().lower() in {"exit", "quit"}:
            print("Jarvis offline.")
            break
        result = assistant.process_command(text)
        print(f"Jarvis: {result['message']}")


if __name__ == "__main__":
    run_cli()
