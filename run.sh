#!/bin/bash
# ==============================================================================
# Claude Voice Assistant - Run Script
# ==============================================================================
# This script activates the virtual environment and starts the server.
#
# Make sure to set your API key first:
#   export ANTHROPIC_API_KEY='your-api-key-here'
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

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY is not set."
    echo ""
    echo "Please set it with:"
    echo "  export ANTHROPIC_API_KEY='your-api-key-here'"
    echo ""
    read -p "Or enter it now: " ANTHROPIC_API_KEY
    export ANTHROPIC_API_KEY
    echo ""
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
