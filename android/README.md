from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from backend.assistant import JarvisAssistant


class JarvisDesktopApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Jarvis Desktop Assistant")
        self.root.geometry("900x600")

        self.assistant = JarvisAssistant()

        self.output = tk.Text(root, wrap="word", state="disabled", bg="#101820", fg="#F4F7FA", font=("Segoe UI", 12))
        self.output.pack(fill="both", expand=True, padx=12, pady=(12, 8))

        input_frame = tk.Frame(root)
        input_frame.pack(fill="x", padx=12, pady=(0, 12))

        self.command_entry = tk.Entry(input_frame, font=("Segoe UI", 12))
        self.command_entry.pack(side="left", fill="x", expand=True)
        self.command_entry.bind("<Return>", self.handle_submit)

        self.send_button = ttk.Button(input_frame, text="Send", command=self.handle_submit)
        self.send_button.pack(side="right", padx=(10, 0))

        self.append_output("Jarvis ready. Ask me anything.")

    def append_output(self, text: str) -> None:
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def handle_submit(self, event=None):
        command = self.command_entry.get().strip()
        if not command:
            return

        self.append_output(f"You: {command}")
        self.command_entry.delete(0, "end")

        result = self.assistant.process_command(command)
        self.append_output(f"Jarvis: {result['message']}")


if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisDesktopApp(root)
    root.mainloop()
