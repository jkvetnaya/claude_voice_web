#!/bin/bash
# ==============================================================================
# Claude Voice Assistant - Run Script
# ==============================================================================
# This script activates the virtual environment and starts the server.
# API key is read from .env file automatically.
#
# Usage:
#   chmod +x run.sh
#   ./run.sh
# ==============================================================================

echo "=============================================="
echo "  Claude Voice Assistant"
echo "=============================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found."
    echo "Please run ./setup.sh first."
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found."
    echo "Please create it from the example:"
    echo "  cp .env.example .env"
    echo "  nano .env"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo "Starting server..."
echo "Open http://localhost:5000 in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=============================================="
echo ""

python server.py
