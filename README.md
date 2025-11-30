# Claude Voice Assistant - Web Edition

A beautiful, browser-based voice assistant that lets you talk to Claude. Runs entirely on your local machine with **persistent conversation history**.

![Screenshot placeholder - the interface has a dark theme with a glowing microphone button]

## Features

- 🎤 **One-click recording** - Click the mic button or press Space to record
- 🎨 **Beautiful dark UI** - Modern, polished interface that's easy on the eyes
- 💬 **Conversation memory** - Claude remembers context throughout your session
- 💾 **Persistent history** - Conversations are saved to disk and survive restarts
- 📚 **Multiple sessions** - Switch between different conversation threads
- 🔒 **Local processing** - Audio transcription happens on your machine
- ⌨️ **Keyboard shortcuts** - Press Space to start/stop recording

## Requirements

- Python 3.8+
- A microphone
- An Anthropic API key
- A modern web browser (Chrome, Firefox, Safari, Edge)

## Quick Start

### Option 1: Automated Setup (Recommended)

**On macOS/Linux:**
```bash
cd claude_voice_web
chmod +x setup.sh run.sh
./setup.sh
```

**On Windows:**
```
Double-click setup.bat
```

Then set your API key and run:

**macOS/Linux:**
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
./run.sh
```

**Windows:**
```
set ANTHROPIC_API_KEY=your-api-key-here
run.bat
```

### Option 2: Manual Setup

```bash
cd claude_voice_web

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate        # macOS/Linux
# OR
venv\Scripts\activate.bat       # Windows

# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY='your-api-key-here'  # macOS/Linux
# OR
set ANTHROPIC_API_KEY=your-api-key-here       # Windows

# Run
python server.py
```

### Open the App

Open your browser and go to: **http://localhost:5000**

## Usage

1. **Click the microphone button** (or press Space)
2. **Speak your message**
3. **Click again** (or press Space) to stop recording
4. **Wait** for Claude to respond

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Toggle recording |

### Controls

- **🎤 Microphone button** - Start/stop recording
- **📜 History button** - View and switch between saved conversations
- **➕ New Chat button** - Start a fresh conversation
- **🗑️ Clear button** - Clear current conversation history

## Conversation Persistence

Your conversations are **automatically saved** to `conversation_history.json` in the application folder. This means:

- ✅ Conversations survive server restarts
- ✅ You can close the browser and come back later
- ✅ Multiple conversation threads are supported
- ✅ Up to 100 messages per conversation (configurable)

### Managing Sessions

- Click **"History"** to see all saved conversations
- Click **"New Chat"** to start a fresh conversation
- Your current session is automatically restored when you reopen the app

## Configuration

You can customize the server with environment variables:

```bash
# Whisper model (tiny, base, small, medium, large)
export WHISPER_MODEL="base"

# Claude model
export CLAUDE_MODEL="claude-sonnet-4-5-20250514"

# Then start the server
python server.py
```

### Whisper Model Comparison

| Model | Speed | Accuracy | VRAM |
|-------|-------|----------|------|
| `tiny` | ⚡⚡⚡⚡ | ★★☆☆ | ~1 GB |
| `base` | ⚡⚡⚡ | ★★★☆ | ~1 GB |
| `small` | ⚡⚡ | ★★★★ | ~2 GB |
| `medium` | ⚡ | ★★★★★ | ~5 GB |
| `large` | 🐢 | ★★★★★ | ~10 GB |

For most users, `base` (default) is recommended.

## Project Structure

```
claude_voice_web/
├── setup.sh                     # Setup script (macOS/Linux)
├── setup.bat                    # Setup script (Windows)
├── run.sh                       # Run script (macOS/Linux)
├── run.bat                      # Run script (Windows)
├── requirements.txt             # Python dependencies
├── server.py                    # Flask backend server
├── index.html                   # Web interface
├── conversation_history.json    # Auto-generated: saved conversations
├── venv/                        # Auto-generated: virtual environment
└── README.md                    # This file
```

## Troubleshooting

### "Could not access microphone"

Your browser needs permission to use the microphone:
- Click the lock/info icon in your browser's address bar
- Allow microphone access for localhost

### "Could not connect to server"

Make sure:
1. The server is running (`python server.py`)
2. You're accessing `http://localhost:5000` (not `https://`)

### Slow transcription

- Use a smaller Whisper model: `export WHISPER_MODEL=tiny`
- If you have an NVIDIA GPU, ensure CUDA is installed for acceleration

### API errors

- Check your `ANTHROPIC_API_KEY` is set correctly
- Verify your API key has available credits at [console.anthropic.com](https://console.anthropic.com)

## Advanced: Running on a Different Port

```bash
# Edit server.py, change the last line:
app.run(host='0.0.0.0', port=8080, debug=False)
```

## Advanced: Accessing from Other Devices

By default, the server binds to `0.0.0.0`, so you can access it from other devices on your network:

1. Find your computer's local IP (e.g., `192.168.1.100`)
2. Open `http://192.168.1.100:5000` from another device

Note: Microphone access requires HTTPS on non-localhost origins in most browsers. For local network use, you may need to set up a self-signed certificate.

## Tech Stack

- **Backend**: Python, Flask
- **Transcription**: OpenAI Whisper (local)
- **AI**: Anthropic Claude API
- **Frontend**: Vanilla HTML/CSS/JS (no build step required!)

## License

MIT License - feel free to modify and use as you wish!
