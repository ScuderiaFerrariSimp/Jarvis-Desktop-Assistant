# JARVIS — Phase 1 (UI + minimal test backend)

A working desktop shell with a real (if minimal) AI backend wired in:
type a message in the composer, it goes to Claude, the reply comes back
into the transcript, and the orb reacts (idle → speaking → idle).

This is intentionally small — one provider, no memory, no voice, no
routing logic. It exists so you can confirm the whole pipe works
(UI → bridge → provider → UI) before building out the real AI Manager.

## Setup

```
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and paste in your own key:

```
ANTHROPIC_API_KEY=sk-ant-...
```

## Run

```
python main.py
```

Frameless window opens. Type in the composer bar and press Enter/Send.
Esc to quit.

## What's real vs. what's still a stub

**Real and working:**
- `main.py` — desktop shell, registers a `QWebChannel` bridge
- `backend/bridge.py` — the `Bridge` QObject; `send_message` is called
  from JS, calls the AI Manager, emits the reply back
- `backend/ai_manager.py` — thin wrapper holding "the current provider"
- `backend/providers/anthropic_provider.py` — actual Claude API call via
  the official SDK
- `backend/config.py` — loads `.env`, no hardcoded keys anywhere
- `ui/orb.html` — composer calls `window.bridge.send_message(text)` for
  real; orb reacts to real reply timing, not a fake delay

**Still stubs / not built yet (later phases per Phases.md):**
- Voice (Phase 2) — composer is a deliberate text fallback until then
- Memory (Phase 2) — no conversation history is persisted or sent back
  to the model; each message is a fresh, context-free call
- Multiple providers / routing (Phase 5) — only Anthropic is wired up;
  `backend/providers/base.py` is the interface future providers
  (Ollama, Gemini, etc.) should implement
- Automation, plugins (Phase 3) — not present

## File structure

```
jarvis_app/
├── main.py                          # desktop shell + QWebChannel wiring
├── .env.example                     # copy to .env, add your key
├── .gitignore                       # keeps .env out of git
├── requirements.txt
├── ui/
│   └── orb.html                     # orb + transcript + composer (frontend)
└── backend/
    ├── config.py                    # .env loading
    ├── ai_manager.py                # holds the active provider
    ├── bridge.py                    # QWebChannel bridge (JS <-> Python)
    └── providers/
        ├── base.py                  # Provider interface (abstract)
        └── anthropic_provider.py    # Claude implementation
```

## Known limitations (by design, for now)

- No conversation memory — every message is stateless. Fine for testing
  the pipe works; not fine for actual use.
- Single provider, no fallback/routing.
- `Bridge.send_message` calls the Anthropic SDK synchronously, which
  blocks the Qt event loop briefly per request. Rules.md calls for
  "async-first" — this is the one deliberate shortcut, flagged so it
  doesn't get mistaken for the final design. Worth fixing before Phase 2.
