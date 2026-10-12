# Jarvis AI Assistant - Complete Setup and Usage Guide

## Prerequisites

- Python 3.9+
- Windows 10/11 (or Linux/macOS with adjustments)
- Microphone (for voice features)
- Internet connection (for ChatGPT and search)

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

Edit `.env` and add your credentials:

```
# For ChatGPT mode (optional but recommended)
OPENAI_API_KEY=sk-...

# For Google Search (optional)
GOOGLE_API_KEY=...
GOOGLE_SEARCH_ENGINE_ID=...
```

## Getting API Credentials

### OpenAI API Key (ChatGPT)

1. Go to [OpenAI Platform](https://platform.openai.com/account/api-keys)
2. Sign up or log in
3. Create a new API key
4. Copy the key to `.env` as `OPENAI_API_KEY`

### Google Custom Search API

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create a new project
3. Enable "Custom Search API"
4. Create an API key
5. Go to [Google Custom Search](https://cse.google.com/cse/)
6. Create a new search engine
7. Copy the Search Engine ID

### Wikipedia Search (Free - No API Key)

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

## Features

### Text Commands

- **Greeting**: `hello`, `hi`, `hey`
- **Time**: `what time is it`, `current date`
- **Open Apps**: `open notepad`, `open chrome`
- **Search**: `search python programming`, `find machine learning`
- **Wikipedia**: `search machine learning on wikipedia`
- **AI Chat** (with ChatGPT): Any natural language question

### Voice Features

- **Voice Input**: Click "🎧 Listen" to speak commands
- **Voice Output**: Toggle "🎙 Voice: On/Off" to hear responses
- Requires microphone and internet (for Google Speech-to-Text)

### Modes

#### Local Mode (Default)

- Intent-based command routing
- System control (open apps, run commands)
- Search integration (Google + Wikipedia)
- Fast, no API keys needed
- Limited conversational ability

#### AI Mode (ChatGPT)

- Full ChatGPT integration for open-ended questions
- Context-aware responses
- Conversation history support
- Requires OpenAI API key
- Better for natural language understanding

## Testing Commands

### Text-Based

```
You: hello
Jarvis: Hi there. How can I assist you today?

You: what time is it
Jarvis: The current time is 3:45 PM. Today is Monday, October 12, 2026.

You: open notepad
Jarvis: Opening notepad.

You: search machine learning
Jarvis: Found 5 results for 'machine learning'...
```

### ChatGPT Mode

```
You: explain quantum computing
Jarvis: Quantum computing is a revolutionary form of computing that uses quantum bits...

You: tell me a joke
Jarvis: Why don't scientists trust atoms? Because they make up everything!
```

### Voice Mode

1. Toggle "🎙 Voice: On"
2. Click "🎧 Listen"
3. Speak your command
4. Jarvis responds with text and voice

## Architecture

```
┌────────────────────────────────────────┐
│       Desktop GUI (Tkinter)             │
│  ┌──────────────────────────────────┐   │
│  │ Chat Display & Input              │   │
│  │ Voice Controls (Listen/Speak)     │   │
│  │ Mode Toggle (AI/Local)            │   │
│  │ Status Display                    │   │
│  └──────────────────────────────────┘   │
└────────────────────┬──────────────────┘
                     │ HTTP REST API
                     ▼
┌────────────────────────────────────────┐
│      FastAPI Backend Server             │
│      (http://127.0.0.1:8000)            │
│  ┌──────────────────────────────────┐   │
│  │ /command - Process text           │   │
│  │ /voice - Speech-to-text           │   │
│  │ /speak - Text-to-speech           │   │
│  │ /health - Backend status          │   │
│  └──────────────────────────────────┘   │
└────────────────────┬──────────────────┘
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Jarvis   │  │ OpenAI   │  │ Search   │
│ Assistant│  │ ChatGPT  │  │ Engines  │
│(Local)   │  │ API      │  │(Google + │
│          │  │          │  │Wikipedia)│
└──────────┘  └──────────┘  └──────────┘
```

## Project Structure

```
jarvis-ai-assistant/
├── backend/
│   ├── __init__.py
│   ├── assistant.py           # Main Jarvis logic
│   ├── config.py              # Settings
│   ├── system_controller.py   # OS control
│   ├── voice_manager.py       # Speech-to-text & TTS
│   ├── search_engine.py       # Search integration
│   ├── api/
│   │   └── server.py          # FastAPI server
│   └── ai/
│       ├── intent_model.py    # Intent detection
│       └── providers.py       # AI providers (Local, OpenAI)
├── desktop/
│   └── main.py                # Desktop GUI app
├── android/                   # Android app (coming soon)
├── tests/                     # Test suite
├── requirements.txt           # Python dependencies
├── .env.example               # Configuration template
├── SETUP.md                   # This file
└── README.md                  # Project overview
```

## Troubleshooting

### Backend Won't Start

```bash
pip install -r requirements.txt
python -m compileall backend
python -m backend
```

### Desktop App Can't Connect

- Ensure backend is running
- Check status shows "Online"
- Try "Test API" button
- Restart both apps

### ChatGPT Mode Returns Error

- Verify `OPENAI_API_KEY` is set in `.env`
- Check API key is valid at https://platform.openai.com/account/api-keys
- Ensure sufficient API credits
- Check internet connection

### Voice Features Not Working

- Check microphone is connected
- Test microphone in Windows Sound settings
- Verify `speechrecognition` package installed
- Run: `pip install --upgrade speechrecognition pyttsx3 pyaudio`

### Search Returns No Results

- Google Search requires valid API credentials
- Wikipedia search should work without credentials
- Check internet connection
- Try simpler search terms

## Next Steps

✅ Text-based commands (working)  
✅ ChatGPT integration (working)  
✅ Voice input/output (working)  
✅ Search integration (working)  
⏳ Android mobile app  
⏳ Conversation memory/database  
⏳ Wake word detection  
⏳ Advanced automation  
⏳ Local AI model support (Llama, Mistral)  

## License

MIT

## Support

For issues or questions:
- Check SETUP.md Troubleshooting section
- Review .env configuration
- Check backend logs
- Visit GitHub repository for more info
