# 🤖 JARVIS

> **An open-source, lightweight AI desktop assistant built for
> productivity, automation, and privacy.**

JARVIS is a modular desktop AI assistant that combines **offline AI
models** with **cloud AI providers**, allowing users to choose between
privacy, speed, and intelligence while maintaining minimal resource
usage.

**Status:** 🚧 Early Development

------------------------------------------------------------------------

# ✨ Vision

Build a native desktop AI assistant that is:

-   Offline-first
-   Cloud-enhanced
-   Lightweight
-   Privacy-focused
-   Modular
-   Plugin-based
-   Voice-enabled
-   Open Source

------------------------------------------------------------------------

# 🚀 Planned Features

## AI

-   Offline models (Ollama)
-   Cloud AI providers
-   Intelligent model routing
-   Streaming responses
-   Multi-model support
-   Long-term memory

Supported local models: - Gemma - Mistral - DeepSeek - Qwen - Llama -
Phi - Granite

Supported cloud providers: - OpenAI - NVIDIA Nemotron - Anthropic -
Google Gemini - xAI - OpenRouter - Together AI - Azure OpenAI - Any
OpenAI-compatible endpoint

## Voice

-   Wake word
-   Clap detection (optional)
-   Push-to-talk
-   Speech-to-text
-   Text-to-speech

## Desktop Automation

-   Launch applications
-   Window management
-   File management
-   Clipboard
-   Screenshots
-   Notifications
-   System controls

## Plugins

-   Weather
-   News
-   Formula 1
-   Browser
-   Calendar
-   Spotify
-   OCR
-   PDF Reader
-   Notes
-   Timers
-   Image Generation

------------------------------------------------------------------------

# 🏗 Architecture

``` text
                 UI (PySide6)

                       │

              Core Controller

                       │

      ┌────────────────┼────────────────┐
      │                │                │

 AI Router      Memory Manager    Tool Manager

      │                │                │

Offline AI      SQLite / Vector      Plugins

      │                │                │

 Cloud Providers     Automation     Desktop APIs
```

------------------------------------------------------------------------

# ⚙️ Technology Stack

## Backend

-   Python
-   AsyncIO
-   FastAPI
-   SQLite
-   SQLAlchemy
-   Pydantic

## Desktop

-   PySide6 (Qt)

## Speech

-   Faster-Whisper
-   Piper
-   openWakeWord

------------------------------------------------------------------------

# 📌 Roadmap

## Phase 1

-   [ ] Native desktop app
-   [ ] Chat interface
-   [ ] Local AI support
-   [ ] Cloud AI support

## Phase 2

-   [ ] Voice interaction
-   [ ] Wake word
-   [ ] Memory
-   [ ] System tray

## Phase 3

-   [ ] Desktop automation
-   [ ] Plugin framework
-   [ ] Performance optimization

## Phase 4

-   [ ] Vision
-   [ ] RAG
-   [ ] Mobile companion
-   [ ] Smart home support

------------------------------------------------------------------------

# 🤝 Contributing

Contributions, feature requests, bug reports, and pull requests are
welcome.

------------------------------------------------------------------------

# 📄 License

License: TBD

------------------------------------------------------------------------

*"The best assistant is the one you forget is running---until you need
it."*
