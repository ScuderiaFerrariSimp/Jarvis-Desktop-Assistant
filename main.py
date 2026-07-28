"""
JARVIS — desktop shell (Phase 1: UI + minimal test backend)

Loads the orb UI (ui/orb.html) into a native, borderless, always-blue
desktop window using PySide6 + QWebEngineView, and wires it to a real
(if minimal) AI Manager via QWebChannel so the composer actually talks
to Claude.

Setup:
    pip install -r requirements.txt
    cp .env.example .env   # then paste your ANTHROPIC_API_KEY into .env

Run:
    python main.py
"""

import json
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtGui import QIcon

from backend import Bridge


UI_DIR = Path(__file__).parent / "ui"
ORB_HTML = UI_DIR / "orb.html"


class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("JARVIS")
        self.resize(900, 700)

        # Frameless, dark, floats like a HUD panel rather than a normal app window.
        # Comment out FramelessWindowHint while developing if you want normal
        # window controls (resize/close) back for convenience.
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

        self.view = QWebEngineView(self)

        # --- Backend wiring -------------------------------------------
        # Bridge exposes send_message(text) to JS, and emits reply_ready /
        # error_occurred back to Python when the AI Manager responds.
        self.bridge = Bridge()
        self.bridge.reply_ready.connect(self._on_reply_ready)
        self.bridge.error_occurred.connect(self._on_error)

        self.channel = QWebChannel()
        self.channel.registerObject("bridge", self.bridge)
        self.view.page().setWebChannel(self.channel)
        # -----------------------------------------------------------------

        self.view.load(QUrl.fromLocalFile(str(ORB_HTML.resolve())))
        self.setCentralWidget(self.view)

    def _on_reply_ready(self, text: str) -> None:
        self.add_assistant_message(text)
        self.set_orb_mode("idle")

    def _on_error(self, message: str) -> None:
        self.add_assistant_message(f"[error] {message}")
        self.set_orb_mode("idle")

    def set_orb_mode(self, mode: str) -> None:
        """Drive the orb's visual state from Python.

        mode: one of "idle", "listening", "speaking"
        """
        if mode not in {"idle", "listening", "speaking"}:
            raise ValueError(f"Unknown orb mode: {mode}")
        self.view.page().runJavaScript(f"window.setOrbMode('{mode}')")

    def add_user_message(self, text: str) -> None:
        """Push a user-authored line into the transcript panel."""
        safe = json.dumps(text)  # json.dumps gives us a safely-escaped JS string literal
        self.view.page().runJavaScript(f"window.addUserMessage({safe})")

    def add_assistant_message(self, text: str) -> None:
        """Push an assistant-authored line into the transcript panel.

        BACKEND TODO: call this with the AI Manager's response once it exists,
        e.g. window.add_assistant_message(ai_manager.reply(user_text))
        """
        safe = json.dumps(text)
        self.view.page().runJavaScript(f"window.addAssistantMessage({safe})")

    # QWebChannel bridge is registered in __init__ above. See backend/bridge.py
    # for the Python side, and ui/orb.html (search "QWebChannel bridge") for
    # the matching JS side that calls window.bridge.send_message(text).

    def keyPressEvent(self, event):
        # Esc to quit — since the window is frameless, there's no close button yet.
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("JARVIS")

    window = JarvisWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
