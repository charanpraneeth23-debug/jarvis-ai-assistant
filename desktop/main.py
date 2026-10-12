from __future__ import annotations

import json
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext

import requests


class JarvisDesktopApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Jarvis Desktop Assistant")
        self.root.geometry("980x680")
        self.root.configure(bg="#0b1020")

        self.backend_url = "http://127.0.0.1:8000"

        self.frame = tk.Frame(root, bg="#0b1020")
        self.frame.pack(fill="both", expand=True, padx=18, pady=18)

        title = tk.Label(
            self.frame,
            text="JARVIS",
            bg="#0b1020",
            fg="#5eead4",
            font=("Segoe UI", 26, "bold"),
        )
        title.pack(anchor="w", pady=(0, 12))

        status_frame = tk.Frame(self.frame, bg="#121a2e", bd=1, relief="solid")
        status_frame.pack(fill="x", pady=(0, 12))

        self.status_label = tk.Label(
            status_frame,
            text="Status: Offline",
            bg="#121a2e",
            fg="#f8fafc",
            font=("Segoe UI", 12),
            padx=12,
            pady=10,
        )
        self.status_label.pack(anchor="w")

        self.chat_box = scrolledtext.ScrolledText(
            self.frame,
            width=120,
            height=22,
            bg="#0f172a",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            font=("Segoe UI", 11),
            state="disabled",
            wrap=tk.WORD,
        )
        self.chat_box.pack(fill="both", expand=True)

        input_frame = tk.Frame(self.frame, bg="#0b1020")
        input_frame.pack(fill="x", pady=(12, 0))

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

        bottom_row = tk.Frame(self.frame, bg="#0b1020")
        bottom_row.pack(fill="x", pady=(12, 0))

        self.voice_btn = ttk.Button(bottom_row, text="🎙 Speak", command=self.on_voice)
        self.voice_btn.pack(side="left")

        self.test_btn = ttk.Button(bottom_row, text="Test API", command=self.check_backend)
        self.test_btn.pack(side="left", padx=(10, 0))

        self.append_message("Jarvis ready.")
        self.check_backend()

    def append_message(self, text: str) -> None:
        self.chat_box.configure(state="normal")
        self.chat_box.insert(tk.END, text + "\n")
        self.chat_box.see(tk.END)
        self.chat_box.configure(state="disabled")

    def set_status(self, status: str) -> None:
        self.status_label.config(text=f"Status: {status}")

    def check_backend(self) -> None:
        def worker() -> None:
            try:
                response = requests.get(f"{self.backend_url}/health", timeout=3)
                if response.status_code == 200:
                    self.root.after(0, lambda: self.set_status("Online"))
                    self.root.after(0, lambda: self.append_message("[System] Backend connected."))
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
                payload = {"text": command}
                response = requests.post(f"{self.backend_url}/command", json=payload, timeout=6)
                if response.status_code == 200:
                    data = response.json()
                    result = data.get("message", "No response.")
                else:
                    result = f"Backend error: {response.status_code}"
            except Exception as exc:  # pragma: no cover
                result = f"Connection error: {exc}"

            self.root.after(0, lambda: self.append_message(f"Jarvis: {result}"))
            self.root.after(0, lambda: self.set_status("Online"))

        threading.Thread(target=worker, daemon=True).start()

    def on_voice(self) -> None:
        self.append_message("[Voice] Microphone support can be connected here.")


def main() -> None:
    root = tk.Tk()
    app = JarvisDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
