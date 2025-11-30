#!/bin/bash
# ==============================================================================
# Claude Voice Assistant - Setup Script
# ==============================================================================
# This script creates a virtual environment and installs all dependencies.
#
# Usage:
#   chmod +x setup.sh
#   ./setup.sh
#
# After setup, activate the environment with:
#   source venv/bin/activate
#
# Then run the server with:
#   python server.py
# ==============================================================================

set -e  # Exit on error

echo "=============================================="
echo "  Claude Voice Assistant - Setup"
echo "=============================================="
echo ""

# Check for Python
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "❌ Python not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
$PYTHON -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📥 Installing dependencies (this may take a few minutes)..."
echo "   - Flask (web server)"
echo "   - flask-cors (cross-origin support)"
echo "   - openai-whisper (speech recognition)"
echo "   - anthropic (Claude API)"
echo "   - soundfile (audio processing)"
echo ""

pip install flask flask-cors openai-whisper anthropic

echo ""
echo "=============================================="
echo "  ✅ Setup Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo ""
echo "  1. Set your Anthropic API key:"
echo "     export ANTHROPIC_API_KEY='your-api-key-here'"
echo ""
echo "  2. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  3. Run the server:"
echo "     python server.py"
echo ""
echo "  4. Open http://localhost:5000 in your browser"
echo ""
echo "=============================================="
