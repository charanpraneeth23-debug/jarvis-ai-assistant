from __future__ import annotations

import logging

try:
    import pyttsx3
except Exception:  # pragma: no cover
    pyttsx3 = None

try:
    import speech_recognition as sr
except Exception:  # pragma: no cover
    sr = None


class VoiceManager:
    def __init__(self) -> None:
        self.engine = None
        self.recognizer = None

        if pyttsx3 is not None:
            self.engine = pyttsx3.init()
        if sr is not None:
            self.recognizer = sr.Recognizer()

    def speak(self, text: str) -> None:
        if self.engine is None:
            logging.info("Text-to-speech is not available. Message: %s", text)
            return
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_once(self) -> str:
        if self.recognizer is None or sr is None:
            return ""

        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            return self.recognizer.recognize_google(audio)
        except Exception:  # pragma: no cover
            return ""

    def available(self) -> bool:
        return self.engine is not None and self.recognizer is not None
