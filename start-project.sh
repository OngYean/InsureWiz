#!/bin/bash
# 🚀 Starting InsureWiz Project...
echo
cat <<EOM
This script will start both the backend AI server and frontend

📋 Prerequisites:
- Python 3.8+ installed
- Node.js 18+ installed
- Google AI Studio API key configured
EOM

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed or not in PATH"
    echo "Please install Node.js 18+ and try again"
    exit 1
fi

echo "✅ Prerequisites check passed!"
echo

# Start backend in a new terminal window
if command -v gnome-terminal &> /dev/null; then
    echo "🐍 Starting AI Backend Server..."
    gnome-terminal -- bash -c "cd backend && ./run.sh; exec bash"
elif command -v x-terminal-emulator &> /dev/null; then
    echo "🐍 Starting AI Backend Server..."
    x-terminal-emulator -e "bash -c 'cd backend && ./run.sh; exec bash'"
else
    echo "🐍 Starting AI Backend Server... (run manually if no terminal emulator found)"
    (cd backend && ./run.sh &)
fi

# Wait a moment for backend to start
sleep 3

# Start frontend in a new terminal window
if command -v gnome-terminal &> /dev/null; then
    echo "🌐 Starting Frontend..."
    gnome-terminal -- bash -c "cd frontend && npx next dev; exec bash"
elif command -v x-terminal-emulator &> /dev/null; then
    echo "🌐 Starting Frontend..."
    x-terminal-emulator -e "bash -c 'cd frontend && npx next dev; exec bash'"
else
    echo "🌐 Starting Frontend... (run manually if no terminal emulator found)"
    (cd frontend && npx next dev &)
fi

echo
cat <<EOM
🎉 Both servers are starting in separate windows!

📡 Backend: http://localhost:8000
🌐 Frontend: http://localhost:3000
📚 API Docs: http://localhost:8000/docs

💡 Tips:
- Backend window: Press Ctrl+C to stop the AI server
- Frontend window: Press Ctrl+C to stop the web app
- Close these windows to stop the servers
EOM
