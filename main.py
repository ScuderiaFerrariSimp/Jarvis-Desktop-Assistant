"""
JARVIS — desktop shell (Phase 1: UI only)

Loads the orb UI (ui/orb.html) into a native, borderless, always-blue
desktop window using PySide6 + QWebEngineView.

Run:
    python main.py

Requires:
    pip install PySide6 PySide6-Addons
"""

import json
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QIcon


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
        self.view.load(QUrl.fromLocalFile(str(ORB_HTML.resolve())))
        self.setCentralWidget(self.view)

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

    # BACKEND TODO: register a QWebChannel here so JS can call Python directly
    # (e.g. when the composer's Send button is clicked), instead of Python only
    # pushing one-way into the page. Rough shape:
    #
    #   from PySide6.QtWebChannel import QWebChannel
    #   self.channel = QWebChannel()
    #   self.channel.registerObject("bridge", some_bridge_object)
    #   self.view.page().setWebChannel(self.channel)
    #
    # `some_bridge_object` would be a QObject subclass with @Slot methods like
    # send_message(text) that hand off to the AI Manager. See ui/orb.html for
    # the matching frontend-side hookup (search "QWebChannel bridge placeholder").

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
