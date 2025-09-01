# InsureWiz Backend Project Structure

This document describes the organized structure of the InsureWiz backend following FastAPI best practices.

## Directory Structure

```
backend/
├── app/                           # Main application package
│   ├── __init__.py               # Package initialization
│   ├── api/                      # API endpoints and routers
│   │   ├── __init__.py
│   │   ├── chat.py              # Chat-related endpoints
│   │   └── health.py            # Health check endpoints
│   ├── core/                     # Core application components
│   │   ├── __init__.py
│   │   ├── app.py               # FastAPI app factory
│   │   └── dependencies.py      # Common dependencies
│   ├── models/                   # Pydantic models and schemas
│   │   ├── __init__.py
│   │   └── chat.py              # Chat-related models
│   ├── services/                 # Business logic services
│   │   ├── __init__.py
│   │   └── ai_service.py        # AI service for chat
│   ├── middleware/               # Custom middleware
│   │   ├── __init__.py
│   │   └── logging.py           # Request/response logging
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py
│   │   ├── logger.py            # Centralized logging
│   │   └── exceptions.py        # Custom exception classes
│   └── config.py                 # Configuration management
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (not in git)
├── env.example                   # Environment variables template
└── PROJECT_STRUCTURE.md          # This file
```

## Key Components

### 1. Configuration (`app/config.py`)
- Centralized configuration management using Pydantic Settings
- Environment variable handling
- CORS and security settings
- AI service configuration

### 2. Core Application (`app/core/app.py`)
- FastAPI application factory
- Middleware configuration
- Router registration
- Exception handling
- Startup/shutdown events

### 3. API Routers (`app/api/`)
- Organized by feature/domain
- Clean separation of concerns
- Proper error handling
- Input validation using Pydantic models

### 4. Models (`app/models/`)
- Pydantic models for request/response validation
- Clear data contracts
- Field validation and documentation

### 5. Services (`app/services/`)
- Business logic implementation
- External service integration (AI, databases, etc.)
- Clean separation from API layer

### 6. Middleware (`app/middleware/`)
- Custom middleware for cross-cutting concerns
- Request/response logging
- Authentication, rate limiting, etc.

### 7. Utilities (`app/utils/`)
- Common utility functions
- Centralized logging configuration
- Custom exception classes

## Benefits of This Structure

1. **Maintainability**: Clear separation of concerns
2. **Scalability**: Easy to add new features and endpoints
3. **Testability**: Isolated components for unit testing
4. **Reusability**: Shared utilities and services
5. **Documentation**: Self-documenting code structure
6. **Best Practices**: Follows FastAPI and Python conventions

## Adding New Features

### New API Endpoint
1. Create router in `app/api/`
2. Add models in `app/models/`
3. Implement business logic in `app/services/`
4. Register router in `app/core/app.py`

### New Service
1. Create service class in `app/services/`
2. Add configuration in `app/config.py` if needed
3. Import and use in API routers

### New Model
1. Create Pydantic model in `app/models/`
2. Use for request/response validation
3. Import in relevant routers

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

# Or using uvicorn directly
uvicorn app.core.app:app --host 0.0.0.0 --port 8000 --reload
```

## Environment Variables

Copy `env.example` to `.env` and configure:
- `GOOGLE_API_KEY`: Your Google Gemini API key
- Other configuration as needed

## Testing

The structure supports easy testing:
- Unit tests for services
- Integration tests for API endpoints
- Mock external dependencies

