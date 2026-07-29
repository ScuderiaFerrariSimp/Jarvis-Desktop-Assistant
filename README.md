# JARVIS — Frontend (Phase 1 UI)

This is the **frontend only**. No AI Manager, no providers, no voice, no
memory — just the desktop shell and the orb UI, fully wired with
placeholder hooks for backend work to plug into later.

## Run it

```
pip install -r requirements.txt
python main.py
```

Frameless window opens. Press **Esc** to quit (no close button yet — that's
a frontend polish item, not a backend one).

## What's actually here

- `main.py` — PySide6 desktop shell. Opens a native window, loads the orb
  UI into a `QWebEngineView`.
- `ui/orb.html` — the entire visual frontend: animated orb (idle /
  listening / speaking states), transcript panel, text composer bar. Pure
  HTML/CSS/JS, no framework.

## What's a stub, waiting for backend

Every integration point is marked with a comment containing `BACKEND TODO`
or `BACKEND HOOK`. Search for those strings in both files to find them.
Specifically:

1. **`main.py` → `set_orb_mode(mode)`**
   Already works standalone. Backend should call this to reflect real
   state, e.g. `window.set_orb_mode("listening")` when the mic opens.

2. **`main.py` → `add_user_message(text)` / `add_assistant_message(text)`**
   Already work standalone. Backend calls these to push real conversation
   turns into the transcript panel instead of the current placeholder text.

3. **`ui/orb.html` → composer `submit` handler**
   Currently fakes a reply after a timeout, purely so the UI can be demoed
   without a backend attached. Replace the fake `setTimeout` block with a
   real call once a `QWebChannel` bridge exists (see next point).

4. **`QWebChannel` bridge (not implemented yet)**
   The clean way for JS to call Python directly (e.g. "user pressed send"
   → Python AI Manager → response) rather than Python only pushing one-way
   into the page. Both files have a commented-out sketch of the wiring
   under `BACKEND TODO`. This is probably the first real backend task.

## Design notes

- Palette, orb states, and animations are deliberately tuned (not default
  gradients) — see the earlier design rationale if you want the token
  values reasoned through again.
- The composer input is a deliberate fallback so the app is usable by text
  even before voice (Phase 2) exists.
