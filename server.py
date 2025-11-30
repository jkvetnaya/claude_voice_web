#!/usr/bin/env python3
"""
Claude Voice Assistant - Web Server
====================================
A Flask-based web server that provides a browser interface for talking to Claude.

Requirements:
    pip install flask flask-cors openai-whisper anthropic python-dotenv

Setup:
    1. Copy .env.example to .env and add your API key:
       cp .env.example .env
       # Edit .env and add your ANTHROPIC_API_KEY
    
    2. Run the server:
       python server.py
    
    3. Open http://localhost:5000 in your browser

The server handles:
    - Receiving audio recordings from the browser
    - Transcribing audio using Whisper
    - Sending messages to Claude API
    - Returning responses to the browser
    - Persisting conversation history to disk
"""

import os
import sys
import json
import tempfile
import base64
import atexit
from pathlib import Path
from datetime import datetime

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Configuration
HISTORY_FILE = Path(__file__).parent / "conversation_history.json"
MAX_HISTORY_MESSAGES = 100  # Increased from 20 to 100 messages per session

# Check dependencies before importing
def check_dependencies():
    """Check that all required packages are installed."""
    missing = []
    
    try:
        import whisper
    except ImportError:
        missing.append("openai-whisper")
    
    try:
        import anthropic
    except ImportError:
        missing.append("anthropic")
    
    if missing:
        print("Missing required packages. Install them with:")
        print(f"  pip install flask flask-cors {' '.join(missing)}")
        sys.exit(1)
    
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("=" * 60)
        print("WARNING: ANTHROPIC_API_KEY environment variable not set.")
        print("Set it with: export ANTHROPIC_API_KEY='your-api-key-here'")
        print("=" * 60)


check_dependencies()

import whisper
import anthropic

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)

# Global variables
whisper_model = None
claude_client = None
conversation_histories = {}  # Store conversations by session ID


def load_conversation_history():
    """Load conversation history from disk."""
    global conversation_histories
    
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                conversation_histories = data.get('conversations', {})
                print(f"✓ Loaded {len(conversation_histories)} conversation(s) from disk")
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠ Could not load history file: {e}")
            conversation_histories = {}
    else:
        print("✓ No existing history file, starting fresh")


def save_conversation_history():
    """Save conversation history to disk."""
    try:
        data = {
            'last_saved': datetime.now().isoformat(),
            'conversations': conversation_histories
        }
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved {len(conversation_histories)} conversation(s) to disk")
    except IOError as e:
        print(f"⚠ Could not save history file: {e}")


# Load history on startup
load_conversation_history()

# Save history on shutdown
atexit.register(save_conversation_history)


def get_whisper_model():
    """Lazy load Whisper model."""
    global whisper_model
    if whisper_model is None:
        model_name = os.environ.get("WHISPER_MODEL", "base")
        print(f"Loading Whisper model '{model_name}'... ", end="", flush=True)
        whisper_model = whisper.load_model(model_name)
        print("Done!")
    return whisper_model


def get_claude_client():
    """Get Claude API client."""
    global claude_client
    if claude_client is None:
        claude_client = anthropic.Anthropic()
    return claude_client


@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_from_directory('.', 'index.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory('static', filename)


@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Transcribe audio using Whisper.
    
    Expects JSON with:
        - audio: base64-encoded audio data (webm format)
    
    Returns:
        - text: transcribed text
    """
    try:
        data = request.get_json()
        
        if 'audio' not in data:
            return jsonify({'error': 'No audio data provided'}), 400
        
        # Decode base64 audio
        audio_data = base64.b64decode(data['audio'])
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as f:
            temp_path = f.name
            f.write(audio_data)
        
        try:
            # Transcribe with Whisper
            model = get_whisper_model()
            result = model.transcribe(temp_path)
            text = result['text'].strip()
            
            return jsonify({'text': text})
        finally:
            # Clean up temp file
            os.unlink(temp_path)
            
    except Exception as e:
        print(f"Transcription error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Send a message to Claude and get a response.
    
    Expects JSON with:
        - message: user's message text
        - session_id: unique session identifier (optional)
    
    Returns:
        - response: Claude's response text
    """
    try:
        data = request.get_json()
        
        if 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        message = data['message']
        session_id = data.get('session_id', 'default')
        
        # Get or create conversation history for this session
        if session_id not in conversation_histories:
            conversation_histories[session_id] = []
        
        history = conversation_histories[session_id]
        
        # Add user message to history
        history.append({
            'role': 'user',
            'content': message
        })
        
        # Get Claude response
        client = get_claude_client()
        response = client.messages.create(
            model=os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5-20250929"),
            max_tokens=2048,
            system="You are a helpful voice assistant. Keep your responses concise and conversational since they will be displayed to a user who just spoke to you. Be friendly, natural, and helpful. Use markdown formatting when appropriate for readability.",
            messages=history
        )
        
        assistant_message = response.content[0].text
        
        # Add assistant response to history
        history.append({
            'role': 'assistant',
            'content': assistant_message
        })
        
        # Limit history size to prevent token overflow
        if len(history) > MAX_HISTORY_MESSAGES:
            history = history[-MAX_HISTORY_MESSAGES:]
            conversation_histories[session_id] = history
        
        # Save to disk after each exchange
        save_conversation_history()
        
        return jsonify({'response': assistant_message})
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """
    Send a message to Claude and stream the response.
    
    Expects JSON with:
        - message: user's message text
        - session_id: unique session identifier (optional)
    
    Returns:
        - Server-sent events with streamed response chunks
    """
    from flask import Response, stream_with_context
    
    data = request.get_json()
    
    if 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    
    message = data['message']
    session_id = data.get('session_id', 'default')
    
    # Get or create conversation history for this session
    if session_id not in conversation_histories:
        conversation_histories[session_id] = []
    
    history = conversation_histories[session_id]
    
    # Add user message to history
    history.append({
        'role': 'user',
        'content': message
    })
    
    def generate():
        try:
            client = get_claude_client()
            full_response = ""
            
            # Stream the response
            with client.messages.stream(
                model=os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5-20250929"),
                max_tokens=2048,
                system="You are a helpful voice assistant. Keep your responses concise and conversational since they will be displayed to a user who just spoke to you. Be friendly, natural, and helpful. Use markdown formatting when appropriate for readability.",
                messages=history
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    # Send each chunk as a server-sent event
                    yield f"data: {json.dumps({'chunk': text})}\n\n"
            
            # Add assistant response to history
            history.append({
                'role': 'assistant',
                'content': full_response
            })
            
            # Limit history size
            if len(history) > MAX_HISTORY_MESSAGES:
                conversation_histories[session_id] = history[-MAX_HISTORY_MESSAGES:]
            
            # Save to disk
            save_conversation_history()
            
            # Send done signal
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except Exception as e:
            print(f"Stream error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )


@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear conversation history for a session."""
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        
        if session_id in conversation_histories:
            conversation_histories[session_id] = []
            save_conversation_history()
        
        return jsonify({'status': 'cleared'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'whisper_model': os.environ.get("WHISPER_MODEL", "base"),
        'claude_model': os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5-20250929"),
        'total_sessions': len(conversation_histories)
    })


@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    """List all saved conversation sessions."""
    sessions = []
    for session_id, history in conversation_histories.items():
        if history:  # Only include non-empty sessions
            # Get first user message as preview
            preview = ""
            for msg in history:
                if msg['role'] == 'user':
                    preview = msg['content'][:100] + ('...' if len(msg['content']) > 100 else '')
                    break
            
            sessions.append({
                'session_id': session_id,
                'message_count': len(history),
                'preview': preview
            })
    
    return jsonify({'sessions': sessions})


@app.route('/api/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get conversation history for a specific session."""
    if session_id not in conversation_histories:
        return jsonify({'error': 'Session not found'}), 404
    
    return jsonify({
        'session_id': session_id,
        'messages': conversation_histories[session_id]
    })


@app.route('/api/session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a specific session."""
    if session_id in conversation_histories:
        del conversation_histories[session_id]
        save_conversation_history()
    
    return jsonify({'status': 'deleted'})


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🎙️  Claude Voice Assistant - Web Server")
    print("=" * 60)
    print(f"Whisper model: {os.environ.get('WHISPER_MODEL', 'base')}")
    print(f"Claude model: {os.environ.get('CLAUDE_MODEL', 'claude-sonnet-4-5-20250929')}")
    print("=" * 60)
    print("\nStarting server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    # Pre-load Whisper model
    get_whisper_model()
    
    app.run(host='0.0.0.0', port=5000, debug=False)
