from __future__ import annotations

import os
import platform
import subprocess
from typing import Any, Dict, List


class SystemController:
    def __init__(self) -> None:
        self.system = platform.system().lower()

    def open_application(self, app_name: str) -> Dict[str, Any]:
        try:
            if self.system == "windows":
                os.startfile(app_name)  # type: ignore[attr-defined]
            elif self.system == "darwin":
                subprocess.run(["open", app_name], check=True)
            else:
                subprocess.run(["xdg-open", app_name], check=True)
            return {"success": True, "app": app_name}
        except Exception as exc:  # pragma: no cover - platform-specific
            return {"success": False, "error": str(exc)}

    def run_command(self, command: str) -> Dict[str, Any]:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except Exception as exc:  # pragma: no cover
            return {"success": False, "error": str(exc)}

    def list_common_apps(self) -> List[str]:
        return ["notepad", "chrome", "calc", "cmd", "explorer"]


if __name__ == "__main__":
    controller = SystemController()
    print(controller.list_common_apps())
