from __future__ import annotations

import json
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

import requests


class JarvisDesktopApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Jarvis Desktop Assistant")
        self.root.geometry("1000x750")
        self.root.configure(bg="#0b1020")

        self.backend_url = "http://127.0.0.1:8000"
        self.ai_mode = False
        self.voice_enabled = False

        # Main frame
        self.frame = tk.Frame(root, bg="#0b1020")
        self.frame.pack(fill="both", expand=True, padx=18, pady=18)

        # Title
        title = tk.Label(
            self.frame,
            text="JARVIS",
            bg="#0b1020",
            fg="#5eead4",
            font=("Segoe UI", 26, "bold"),
        )
        title.pack(anchor="w", pady=(0, 12))

        # Status frame
        status_frame = tk.Frame(self.frame, bg="#121a2e", bd=1, relief="solid")
        status_frame.pack(fill="x", pady=(0, 12))

        status_left = tk.Frame(status_frame, bg="#121a2e")
        status_left.pack(fill="x", padx=12, pady=10, side="left")

        self.status_label = tk.Label(
            status_left,
            text="Status: Offline",
            bg="#121a2e",
            fg="#f8fafc",
            font=("Segoe UI", 11, "bold"),
        )
        self.status_label.pack(side="left")

        self.mode_label = tk.Label(
            status_left,
            text="| Mode: Local",
            bg="#121a2e",
            fg="#a1e3d4",
            font=("Segoe UI", 11),
        )
        self.mode_label.pack(side="left", padx=(10, 0))

        self.voice_label = tk.Label(
            status_left,
            text="| Voice: Off",
            bg="#121a2e",
            fg="#a1e3d4",
            font=("Segoe UI", 11),
        )
        self.voice_label.pack(side="left", padx=(10, 0))

        # Chat box
        self.chat_box = scrolledtext.ScrolledText(
            self.frame,
            width=120,
            height=20,
            bg="#0f172a",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            font=("Segoe UI", 10),
            state="disabled",
            wrap=tk.WORD,
        )
        self.chat_box.pack(fill="both", expand=True, pady=(0, 12))

        # Input frame
        input_frame = tk.Frame(self.frame, bg="#0b1020")
        input_frame.pack(fill="x", pady=(0, 12))

        self.command_var = tk.StringVar()
        self.command_entry = tk.Entry(
            input_frame,
            textvariable=self.command_var,
            font=("Segoe UI", 12),
            bg="#111827",
            fg="#f8fafc",
            insertbackground="#f8fafc",
        )
        self.command_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.command_entry.bind("<Return>", self.on_send)

        self.send_btn = ttk.Button(input_frame, text="Send", command=self.on_send)
        self.send_btn.pack(side="right")

        # Control buttons
        button_frame = tk.Frame(self.frame, bg="#0b1020")
        button_frame.pack(fill="x", pady=(0, 12))

        self.test_btn = ttk.Button(button_frame, text="Test API", command=self.check_backend)
        self.test_btn.pack(side="left", padx=(0, 10))

        self.voice_btn = ttk.Button(button_frame, text="🎙 Voice: Off", command=self.toggle_voice)
        self.voice_btn.pack(side="left", padx=(0, 10))

        self.listen_btn = ttk.Button(button_frame, text="🎧 Listen", command=self.on_voice)
        self.listen_btn.pack(side="left", padx=(0, 10))

        self.ai_btn = ttk.Button(button_frame, text="🤖 AI: Off", command=self.toggle_ai_mode)
        self.ai_btn.pack(side="left")

        self.append_message("[Jarvis] Initializing assistant...")
        self.check_backend()

    def append_message(self, text: str) -> None:
        self.chat_box.configure(state="normal")
        self.chat_box.insert(tk.END, text + "\n")
        self.chat_box.see(tk.END)
        self.chat_box.configure(state="disabled")

    def set_status(self, status: str) -> None:
        self.status_label.config(text=f"Status: {status}")

    def update_mode_label(self) -> None:
        mode_text = "AI (ChatGPT)" if self.ai_mode else "Local"
        self.mode_label.config(text=f"| Mode: {mode_text}")
        voice_text = "On" if self.voice_enabled else "Off"
        self.voice_label.config(text=f"| Voice: {voice_text}")

    def toggle_ai_mode(self) -> None:
        self.ai_mode = not self.ai_mode
        mode_text = "🤖 AI: On" if self.ai_mode else "🤖 AI: Off"
        self.ai_btn.config(text=mode_text)
        self.update_mode_label()
        if self.ai_mode:
            self.append_message("[System] Switched to ChatGPT AI Mode. Make sure OPENAI_API_KEY is set in .env")
        else:
            self.append_message("[System] Switched to Local Mode.")

    def toggle_voice(self) -> None:
        self.voice_enabled = not self.voice_enabled
        voice_text = "🎙 Voice: On" if self.voice_enabled else "🎙 Voice: Off"
        self.voice_btn.config(text=voice_text)
        self.update_mode_label()
        if self.voice_enabled:
            self.append_message("[System] Voice mode enabled. Responses will be spoken aloud.")
        else:
            self.append_message("[System] Voice mode disabled.")

    def check_backend(self) -> None:
        def worker() -> None:
            try:
                response = requests.get(f"{self.backend_url}/health", timeout=3)
                if response.status_code == 200:
                    self.root.after(0, lambda: self.set_status("Online"))
                    self.root.after(0, lambda: self.append_message("[System] Backend connected successfully."))
                else:
                    self.root.after(0, lambda: self.set_status("Offline"))
                    self.root.after(0, lambda: self.append_message("[System] Backend responded with an error."))
            except Exception as exc:  # pragma: no cover
                self.root.after(0, lambda: self.set_status("Offline"))
                self.root.after(0, lambda: self.append_message(f"[System] Could not reach backend: {exc}"))

        threading.Thread(target=worker, daemon=True).start()

    def on_send(self, event=None) -> None:
        command = self.command_var.get().strip()
        if not command:
            return
        self.command_var.set("")
        self.append_message(f"You: {command}")
        self.set_status("Processing")

        def worker() -> None:
            try:
                payload = {"text": command, "ai_mode": self.ai_mode}
                response = requests.post(f"{self.backend_url}/command", json=payload, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    result = data.get("message", "No response.")
                else:
                    result = f"Backend error: {response.status_code}"
            except Exception as exc:  # pragma: no cover
                result = f"Connection error: {exc}"

            self.root.after(0, lambda: self.append_message(f"Jarvis: {result}"))
            self.root.after(0, lambda: self.set_status("Online"))

            if self.voice_enabled and result:
                self.root.after(0, lambda: self.speak_response(result))

        threading.Thread(target=worker, daemon=True).start()

    def on_voice(self) -> None:
        self.append_message("[Voice] Listening for voice input...")
        self.set_status("Listening")

        def worker() -> None:
            try:
                response = requests.post(f"{self.backend_url}/voice", timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        recognized_text = data.get("text", "")
                        self.root.after(0, lambda: self.append_message(f"You (voice): {recognized_text}"))
                        result = data.get("response", "No response.")
                        self.root.after(0, lambda: self.append_message(f"Jarvis: {result}"))
                        if self.voice_enabled:
                            self.root.after(0, lambda: self.speak_response(result))
                    else:
                        self.root.after(0, lambda: self.append_message("[Voice] Could not recognize speech."))
                else:
                    self.root.after(0, lambda: self.append_message(f"[Voice] Error: {response.status_code}"))
            except Exception as exc:  # pragma: no cover
                self.root.after(0, lambda: self.append_message(f"[Voice] Error: {exc}"))
            finally:
                self.root.after(0, lambda: self.set_status("Online"))

        threading.Thread(target=worker, daemon=True).start()

    def speak_response(self, message: str) -> None:
        try:
            response = requests.post(f"{self.backend_url}/speak", json={"text": message}, timeout=5)
            if response.status_code != 200:
                self.append_message("[Voice] Could not speak response.")
        except Exception as exc:  # pragma: no cover
            self.append_message(f"[Voice] TTS error: {exc}")


def main() -> None:
    root = tk.Tk()
    app = JarvisDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
