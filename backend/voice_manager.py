from __future__ import annotations

import logging
from typing import Optional

try:
    import pyttsx3
except Exception:  # pragma: no cover
    pyttsx3 = None

try:
    import speech_recognition as sr
except Exception:  # pragma: no cover
    sr = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceManager:
    """Handles speech-to-text and text-to-speech."""

    def __init__(self) -> None:
        self.engine = None
        self.recognizer = None

        if pyttsx3 is not None:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 150)  # Adjust speech rate
            except Exception as exc:  # pragma: no cover
                logger.warning(f"Failed to initialize TTS engine: {exc}")

        if sr is not None:
            try:
                self.recognizer = sr.Recognizer()
            except Exception as exc:  # pragma: no cover
                logger.warning(f"Failed to initialize speech recognizer: {exc}")

    def speak(self, text: str) -> bool:
        """Speak the given text using text-to-speech."""
        if self.engine is None:
            logger.info(f"TTS not available. Message: {text}")
            return False
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as exc:  # pragma: no cover
            logger.error(f"Error speaking: {exc}")
            return False

    def listen_once(self, timeout: int = 10) -> Optional[str]:
        """Listen for speech and convert to text using speech recognition."""
        if self.recognizer is None or sr is None:
            logger.warning("Speech recognition not available.")
            return None

        try:
            with sr.Microphone() as source:
                logger.info("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout)

            try:
                text = self.recognizer.recognize_google(audio)
                logger.info(f"Recognized: {text}")
                return text
            except sr.UnknownValueError:
                logger.warning("Could not understand audio.")
                return None
            except sr.RequestError as exc:  # pragma: no cover
                logger.error(f"Speech recognition API error: {exc}")
                return None
        except Exception as exc:  # pragma: no cover
            logger.error(f"Error listening: {exc}")
            return None

    def is_available(self) -> bool:
        """Check if voice capabilities are available."""
        return self.engine is not None and self.recognizer is not None
