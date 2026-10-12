# Jarvis AI Assistant - Setup and Usage Guide

## Prerequisites

- Python 3.9+
- Windows 10/11 (or Linux/macOS with adjustments)
- Microphone (for voice features)

## Installation

### 1. Clone and Setup

```bash
cd jarvis-ai-assistant
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and add your search credentials:

```
GOOGLE_API_KEY=your-api-key
GOOGLE_SEARCH_ENGINE_ID=your-search-engine-id
```

## Getting Search Credentials

### Google Custom Search API

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create a new project
3. Enable "Custom Search API"
4. Create an API key
5. Go to [Google Custom Search](https://cse.google.com/cse/)
6. Create a new search engine
7. Copy the Search Engine ID

### Alternative: Wikipedia Search (No API Key Needed)

Wikipedia search works out of the box without credentials.

## Running the Application

### Start Backend

```bash
python -m backend
```

Or with FastAPI:

```bash
uvicorn backend.api.server:app --reload
```

The backend will run on `http://127.0.0.1:8000`

### Start Desktop App

In a second terminal:

```bash
python desktop/main.py
```

## Testing Commands

### Text-Based Commands

- **Greeting**: `hello`, `hi`, `hey`
- **Time**: `what time is it`, `current date`
- **Open Apps**: `open notepad`, `open chrome`
- **Search**: `search python programming`, `find machine learning`
- **Wikipedia**: `search machine learning on wikipedia`

### Example Search Commands

```
Search: machine learning
Search: python tutorial
Search: artificial intelligence
```

## Architecture

```
┌─────────────────┐
│  Desktop GUI    │
│  (Tkinter)      │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│  FastAPI Server │
│  :8000          │
└────────┬────────┘
         │
┌────────▼──────────────────────────┐
│      Jarvis Assistant             │
├──────────────────────────────────┤
│ Intent Detection                 │
│ System Control                   │
│ Voice Manager                    │
│ Search Engine Integration        │
└──────────────────────────────────┘
```

## Features

✅ Text-based command input
✅ Web search (Google Custom Search API)
✅ Wikipedia search (free, no API key)
✅ System control (open apps, run commands)
✅ Time and date queries
✅ Intent-based command routing
✅ Extensible backend architecture

## Troubleshooting

### Backend Won't Start

```bash
pip install -r requirements.txt
python -m compileall backend
```

### Desktop App Can't Connect

- Ensure backend is running: `python -m backend`
- Check status shows "Online" in the app
- Clear cache: delete `__pycache__` folders

### Search Returns No Results

- Google Search requires valid API credentials
- Wikipedia search should work without credentials
- Check internet connection

## Next Steps

- Add voice input/output
- Integrate local AI models
- Build Android mobile app
- Add conversation memory
- Implement wake word detection

## Project Structure

```
jarvis-ai-assistant/
├── backend/
│   ├── __init__.py
│   ├── assistant.py          # Main assistant logic
│   ├── config.py             # Settings
│   ├── system_controller.py  # OS control
│   ├── voice_manager.py      # Voice I/O
│   ├── search_engine.py      # Search integration
│   ├── api/
│   │   └── server.py         # FastAPI server
│   └── ai/
│       ├── intent_model.py
│       └── providers.py
├── desktop/
│   └── main.py               # Desktop GUI
├── android/                  # Android app
├── tests/                    # Test suite
├── requirements.txt
├── .env.example
└── README.md
```

## License

MIT
