#!/bin/bash
echo "🚀 Starting InsureWiz AI Chatbot Backend..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    echo "Please copy env.example to .env and add your Google API key"
    cp env.example .env
    echo "📝 Created .env file. Please edit it with your Google API key before continuing."
    echo "💡 Get your API key from: https://makersuite.google.com/app/apikey"
fi

echo
echo "✅ Backend ready! Starting server..."
echo "📡 Server will be available at: http://localhost:8000"
echo "🔗 API Documentation: http://localhost:8000/docs"
echo "💬 Chat endpoint: http://localhost:8000/api/chat"
echo
echo "Press Ctrl+C to stop the server"
echo

# Start the server
python3 run.py
