#!/bin/bash
# RAPID-100 Ollama Setup Script
# Automates setup of Ollama and model creation

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        RAPID-100 Emergency Triage - Ollama Setup          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed!"
    echo
    echo "📥 Please install Ollama first:"
    echo "   1. Visit: https://ollama.ai"
    echo "   2. Download and install for your OS"
    echo "   3. Run: ollama serve (in another terminal)"
    echo
    exit 1
fi

echo "✅ Ollama is installed"
echo

# Check if Ollama server is running
echo "🔍 Checking if Ollama server is running..."
if ! ollama list &> /dev/null; then
    echo "⚠️  Ollama server doesn't appear to be running"
    echo
    echo "Start Ollama in another terminal:"
    echo "   ollama serve"
    echo
    read -p "Press Enter once Ollama is running, or Ctrl+C to exit..."
fi

echo "✅ Ollama server is accessible"
echo

# Navigate to backend directory
echo "📁 Navigating to backend directory..."
cd "$(dirname "$0")" || exit
echo "📍 Current directory: $(pwd)"
echo

# Check if Modelfile exists
if [ ! -f "Modelfile" ]; then
    echo "❌ Modelfile not found!"
    exit 1
fi

echo "✅ Modelfile found"
echo

# Create the rapid-triage model
echo "🤖 Creating RAPID-100 emergency triage model..."
ollama create rapid-triage -f Modelfile

if [ $? -eq 0 ]; then
    echo "✅ Model created successfully!"
else
    echo "❌ Failed to create model"
    exit 1
fi

echo

# Verify model
echo "📋 Verifying model..."
ollama list | grep rapid-triage

echo

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "⚠️  requirements.txt not found"
fi

echo

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           ✅ Setup Complete!                              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo
echo "🚀 Next Steps:"
echo
echo "1. Ensure Ollama is running:"
echo "   ollama serve"
echo
echo "2. Start the backend:"
echo "   python main.py"
echo
echo "3. Run tests:"
echo "   python execute.py"
echo
echo "📖 For more details, see: OLLAMA_INTEGRATION.md"
echo
