# InsureWiz Backend

AI-powered insurance advisor backend built with FastAPI and LangChain.

## Features

- 🤖 AI-powered insurance advice using Google Gemini
- 💬 Conversational chat interface with memory
- 🔒 Secure API endpoints
- 📚 Comprehensive insurance knowledge base
- 🚀 Fast and scalable FastAPI backend

## Prerequisites

- Python 3.8+ (tested with Python 3.13)
- Google Generative AI API key

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit .env and add your Google API key
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

## Getting a Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key to your `.env` file

## Running the Server

### Option 1: Using the startup script
```bash
python start_server.py
```

### Option 2: Using the main entry point
```bash
python run.py
```

### Option 3: Using uvicorn directly
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

- **GET /** - Health check
- **GET /health** - Service status
- **POST /api/chat** - Chat with AI advisor
- **GET /api/conversations/{id}** - Get conversation history
- **DELETE /api/conversations/{id}** - Delete conversation

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example Usage

### Start a chat conversation:
```bash
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is auto insurance?"}'
```

### Get conversation history:
```bash
curl "http://localhost:8000/api/conversations/conv_1"
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed correctly
2. **API key errors**: Verify your Google API key is set in the `.env` file
3. **Port conflicts**: Change the port in the startup script if 8000 is already in use

### Dependency Issues

If you encounter Rust compilation errors:
- The current requirements.txt uses compatible versions that don't require Rust
- If you need newer versions, you may need to install Rust toolchain

## Development

### Project Structure
```
backend/
├── main.py              # Main FastAPI application
├── run.py               # Entry point for running the server
├── start_server.py      # Alternative startup script
├── requirements.txt     # Python dependencies
├── env.example         # Environment variables template
└── README.md           # This file
```

### Adding New Features

1. **New endpoints**: Add routes to `main.py`
2. **New models**: Extend the Pydantic models in `main.py`
3. **New AI features**: Integrate additional LangChain components

## License

This project is part of InsureWiz - an AI-powered insurance platform.
